from pypif_sdk.readview import ReadView
from pypif.obj.common import Value
from json import dumps


def query_to_mdf_records(query=None, datasetID=None):
    """Evaluate a query and return a list of MDF records

    If a datasetID is specified by there is no query, a simple
    whole dataset query is formed for the user
    """

    return []


def pif_to_mdf_record(pif_obj, datasetID):
    """Convert a PIF into partial MDF record"""
    res = {}
    res["mdf"] = _to_meta_data(pif, datasetID)
    res["{source_name}"] = _to_user_defined(pif)
    return dumps(res)


def _to_meta_data(pif_obj, datasetID):
    """Convert the meta-data from the PIF into MDF"""
    pif = pif_obj.as_dictionary()
    mdf = {}
    try:
        if pif.get("category") == "system.chemical":
            mdf["title"] = pif["names"][0]  #REQ
            if pif.get("chemicalFormula"):
                mdf["composition"] = pif["chemicalFormula"]
            mdf["acl"] = ["public"] #TODO: Real ACLs
#            mdf["source_name"] = _construct_new_key(mdf["title"])

            mdf["data_contact"] = []  #REQ
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
            
            mdf["data_contributor"] = [{}] #TODO: Real contrib

            mdf["links"] = {
                "landing_page": "https://citrination.com/datasets/{}".format(datasetID),
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
    except KeyError:
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
    cat = name
    if units:
        cat = "_".join([name, units])
    to_remove = ["/", "\\", "*", "^", "#", " ", "\n", "\t"]
    for c in to_remove:
       cat = cat.replace(c, "_")
    return cat


def _extract_key_value(obj):
    """Extract the value from the object and make a descriptive key"""

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
        
    return key, value

