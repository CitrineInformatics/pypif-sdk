from pypif_sdk.readview import ReadView
from pypif.obj.common import Value, ProcessStep
from citrination_client import PifQuery
from ..util.citrination import get_client
from pypif.pif import dumps

import re


def query_to_mdf_records(query=None, dataset_id=None):
    """Evaluate a query and return a list of MDF records

    If a datasetID is specified by there is no query, a simple
    whole dataset query is formed for the user
    """
    if not query and not dataset_id:
        raise ValueError("Either query or datasetID must be specified")
    if not query:
        query = PifQuery(include_datasets=[dataset_id])
    client = get_client()
    if not client:
        raise ValueError("Unable to create a citrination client; is 'CITRINATION_API_KEY' in the env?")

    result = client.search(query)
    records = []
    for hit in result.hits:
        records.append(pif_to_mdf_record(hit.system, hit.dataset))

    return records


def pif_to_mdf_record(pif_obj, dataset_id):
    """Convert a PIF into partial MDF record"""
    res = {}
    res["mdf"] = _to_meta_data(pif_obj, dataset_id)
    res[res["mdf"]["source_name"]] = _to_user_defined(pif_obj)
    return dumps(res)


def _to_meta_data(pif_obj, dataset_id):
    """Convert the meta-data from the PIF into MDF"""
    pif = pif_obj.as_dictionary()
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

        mdf["acl"] = ["public"] #TODO: Real ACLs
        mdf["source_name"] = _construct_new_key("citrine_" + str(dataset_id))

        if pif.get("contacts"):
            mdf["data_contact"] = []  #TODO: REQ
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
        
        mdf["data_contributor"] = [{}] #TODO: Real contrib

        mdf["links"] = {
            "landing_page": "https://citrination.com/datasets/{}".format(dataset_id),
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


def _to_user_defined(pif):
    """Read the systems in the PIF to populate the user-defined portion"""
    res = {}

    # make a read view to flatten the heirarchy
    rv = ReadView(pif)

    # Iterate over the keys in the read view
    for k in rv.keys():
        name, value = _extract_key_value(rv[k].raw)
        # add any objects that can be extracted
        if name and value is not None:
            res[name] = value
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
