from pypif.obj import System, Reference, Person, Name
from ..func.update_funcs import merge


def parse_name_string(full_name):
    """
    Parse a full name into a Name object

    :param full_name: e.g. "John Smith" or "Smith, John"
    :return: Name object
    """
    name = Name()
    if "," in full_name:
        toks = full_name.split(",")
        name.family = toks[0]
        name.given = ",".join(toks[1:]).strip()
    else:
        toks = full_name.split()
        name.given = toks[0]
        name.family = " ".join(toks[1:]).strip()
    return name


def creator_to_person(creator):
    """
    Parse the creator block in datacite into a Person
    :param creator: block in datacite format
    :return: Person
    """
    name = Name()
    if "creatorName" in creator:
        name = parse_name_string(creator["creatorName"])
    if "familyName" in creator:
        name.family = creator["familyName"]
    if "givenName" in creator:
        name.given = creator["givenName"]

    person = Person(name=name, tags=creator.get("affiliations"))
    return person


def datacite_to_pif_reference(dc):
    """
    Parse a top-level datacite dictionary into a Reference
    :param dc: dictionary containing datacite metadata
    :return: Reference corresponding to that datacite entry
    """
    ref = Reference()
    if dc.get('identifier').get('identifierType') == "DOI":
        ref.doi = dc.get('identifier').get('identifier')
    ref.title = dc.get('title')
    ref.publisher = dc.get('publisher')
    ref.year = dc.get('publicationYear')

    ref.authors = [creator_to_person(x).name for x in dc.get('creators')]

    return ref


def datacite_to_pif(dc):
    """
    Parse a top-level datacite dictionary into a PIF
    :param dc: dictionary containing datacite metadata
    :return: System containing metadata from datacite
    """
    system = System()
    system.references = [datacite_to_pif_reference(dc)]
    return system


def add_datacite(pif, dc):
    """
    Add datacite metadata to an existing pif (out-of-place)
    :param pif: to which metadata should be added
    :param dc: dictionary with datacite metadata
    :return: new PIF with metadata added
    """
    meta_pif = datacite_to_pif(dc)
    return merge(pif, meta_pif)
