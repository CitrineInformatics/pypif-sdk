from pypif_sdk.readview import ReadView
from pypif.obj.common import Value, ProcessStep
from citrination_client import DatasetQuery, Filter, DatasetReturningQuery, DataQuery, PifSystemQuery, \
    PifSystemReturningQuery
from ..util.citrination import get_client
from pypif.pif import dumps

import re


def query_to_mdf_records(query=None, dataset_id=None, mdf_acl=None):
    """Evaluate a query and return a list of MDF records

    If a datasetID is specified by there is no query, a simple
    whole dataset query is formed for the user
    """
    if not query and not dataset_id:
        raise ValueError("Either query or dataset_id must be specified")
    if query and dataset_id:
        raise ValueError("Both query and dataset_id were specified; pick one or the other.")
    if not query:
        query = PifSystemReturningQuery(
            query=DataQuery(
                dataset=DatasetQuery(
                    id=Filter(equal=dataset_id)
                )
            )
        )

    client = get_client()

    if not mdf_acl:
        raise ValueError('Access controls (mdf_acl) must be specified.  Use ["public"] for public access')

    pif_result = client.pif_search(query)
    if len(pif_result.hits) == 0:
        return []

    example_uid = pif_result.hits[0].system.uid
    dataset_query = DatasetReturningQuery(
        query=DataQuery(
            system=PifSystemQuery(
                uid=Filter(equal=example_uid)
            )
        )
    )

    dataset_result = client.dataset_search(dataset_query)

    records = []
    for hit in pif_result.hits:
        records.append(pif_to_mdf_record(hit.system, dataset_result.hits[0], mdf_acl))

    return records


def pif_to_mdf_record(pif_obj, dataset_hit, mdf_acl):
    """Convert a PIF into partial MDF record"""
    res = {}
    res["mdf"] = _to_meta_data(pif_obj, dataset_hit, mdf_acl)
    res[res["mdf"]["source_name"]] = _to_user_defined(pif_obj)
    return dumps(res)


def _to_meta_data(pif_obj, dataset_hit, mdf_acl):
    """Convert the meta-data from the PIF into MDF"""
    pif = pif_obj.as_dictionary()
    dataset = dataset_hit.as_dictionary()
    mdf = {}
    try:
        if pif.get("names"):
            mdf["title"] = pif["names"][0]
        else:
            mdf["title"] = "Citrine PIF " + str(pif["uid"])

        if pif.get("chemicalFormula"):
            mdf["composition"] = pif["chemicalFormula"]
        elif pif.get("composition"):
            mdf["composition"] = ''.join([comp["element"] for comp in pif["composition"] if comp["element"]])
        if not mdf["composition"]:
            mdf.pop("composition")

        mdf["acl"] = mdf_acl
        mdf["source_name"] = _construct_new_key(dataset["name"])

        if pif.get("contacts"):
            mdf["data_contact"] = []
            for contact in pif["contacts"]:
                data_c = {
                    "given_name": contact["name"]["given"],  #REQ
                    "family_name": contact["name"]["family"]  #REQ
                    }
                if contact.get("email"):
                    data_c["email"] = contact.get("email", "")
                if contact.get("orcid"):
                    data_c["orcid"] = contact.get("orcid", "")
                mdf["data_contact"].append(data_c)
            if not mdf["data_contact"]:
                mdf.pop("data_contact")
        
        mdf["data_contributor"] = [{}] 
        if "owner" in dataset:
            name = dataset["owner"].split()
            contributor = {
                "given_name": name[0],
                "family_name": name[1],
                "email": dataset["email"]
            }
            mdf["data_contributor"] = [contributor]

        mdf["links"] = {
            "landing_page": "https://citrination.com/datasets/{}".format(dataset["id"]),
            "publication": []
            }
        if pif.get("references"):
            mdf["author"] = []
            mdf["citation"] = []
            for ref in pif["references"]:
                if ref.get("doi"):
                    mdf["citation"].append(ref["doi"]) #TODO: Make actual citation
                    mdf["links"]["publication"].append(ref["doi"])
                if ref.get("authors"):
                    for author in ref["authors"]:
                        if author.get("given") and author.get("family"):
                            mdf["author"].append({
                                "given_name": author["given"],
                                "family_name": author["family"]
                                })
            # Remove fields if blank
            if not mdf["author"]:
                mdf.pop("author")
            if not mdf["citation"]:
                mdf.pop("citation")
        if not mdf["links"]["publication"]:
            mdf["links"].pop("publication")

        if pif.get("licenses", [{}])[0].get("url"):
            mdf["license"] = pif["licenses"][0]["url"]
        if pif.get("tags"):
            mdf["tags"] = pif["tags"]

    # If required MDF metadata is missing from PIF, abort
    except KeyError as e:
        print("Error: Required MDF metadata", str(e), "not found in PIF", pif["uid"])
        return None

    return mdf


def _to_user_defined(pif_obj):
    """Read the systems in the PIF to populate the user-defined portion"""
    res = {}

    # make a read view to flatten the hierarchy
    rv = ReadView(pif_obj)

    # Iterate over the keys in the read view
    for k in rv.keys():
        name, value = _extract_key_value(rv[k].raw)
        # add any objects that can be extracted
        if name and value is not None:
            res[name] = value

    # Grab interesting values not in the ReadView
    pif = pif_obj.as_dictionary()

    elements = {}
    if pif.get("composition"):
        for comp in pif["composition"]:
            if comp.get("actualAtomicPercent"):
                elements[comp["element"]] = float(comp["actualAtomicPercent"]["value"])
            elif comp.get("actualWeightPercent"):
                elements[comp["element"]] = float(comp["actualWeightPercent"]["value"])
        if elements:
            res["elemental_percent"] = elements
    elif pif.get("chemicalFormula"):
        symbol = ""
        num = ""
        # Chemical formulae are comprised of letters, numbers, and potentially characters we don't care about
        for char in pif["chemicalFormula"]:
            # Uppercase char indicates beginning of new symbol
            if char.isupper():
                # If there is already a symbol in holding, process it
                if symbol:
                    try:
                        elements[symbol] = int(num)
                    # If num is a float, raises ValueError
                    except ValueError:
                        elements[symbol] = float(num) if num else 1
                    symbol = ""
                    num = ""
                symbol += char
            # Lowercase chars or digits are continuations of a symbol
            elif char.islower():
                symbol += char
            elif char.isdigit():
                num += char
            elif char == ".":
                num += char
            # All other chars are not useful
        if elements:
            res["elemental_proportion"] = elements
    return res


def _construct_new_key(name, units=None):
    """Construct an MDF safe key from the name and units"""
    to_replace = ["/", "\\", "*", "^", "#", " ", "\n", "\t", ",", ".", ")", "(", "'", "`", "-"]
    to_remove = ["$", "{", "}"]

    cat = name
    if units:
        cat = "_".join([name, units])
    for c in to_replace:
       cat = cat.replace(c, "_")
    for c in to_remove:
       cat = cat.replace(c, "")

    cat = re.sub('_+','_', cat)

    return cat


def _extract_key_value(obj):
    """Extract the value from the object and make a descriptive key"""
    key = None; value = None

    # Parse a Value object, which includes Properties
    if isinstance(obj, Value):
        key = _construct_new_key(obj.name, obj.units)
        value = None
        if obj.scalars and len(obj.scalars) == 1:
            value = obj.scalars[0].value
        elif obj.scalars:
            value =  [x.value for x in obj.scalars]
        elif obj.vectors and len(obj.vectors) == 1:
            value = [x.value for x in obj.vectors[0]]

    # If there is a process step, pul out its name as the value
    # TODO: resolve duplicates
    if isinstance(obj, ProcessStep):
        key = "Processing"
        value = obj.name
        
    return key, value
