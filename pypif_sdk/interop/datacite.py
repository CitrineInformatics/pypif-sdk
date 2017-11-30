from pypif.obj import System, Reference, Person, Name


def parse_name_string(full_name):
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
    ref = Reference()
    if dc.get('identifier').get('identifierType') == "DOI":
        ref.doi = dc.get('identifier').get('identifier')
    ref.title = dc.get('title')
    ref.publisher = dc.get('publisher')
    ref.year = dc.get('publicationYear')

    ref.authors = [creator_to_person(x).name for x in dc.get('creators')]

    return ref


def datacite_to_pif(dc):
    system = System()
    system.references = [datacite_to_pif_reference(dc)]
    return system
