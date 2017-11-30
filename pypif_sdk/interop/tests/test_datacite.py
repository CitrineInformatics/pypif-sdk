from pypif_sdk.interop.datacite import creator_to_person, datacite_to_pif_reference, add_datacite
from pypif.obj.system import System
from pypif.obj.common import Property, Scalar


def test_simple_creator_name():
    creator = {"creatorName": "John Smith"}
    name = creator_to_person(creator).name
    assert name.family == "Smith"
    assert name.given == "John"


def test_comma_creator_name():
    creator = {"creatorName": "Smith, John"}
    name = creator_to_person(creator).name
    assert name.family == "Smith"
    assert name.given == "John"


def test_middle_creator_name():
    creator = {"creatorName": "Smith, John Jacob"}
    name = creator_to_person(creator).name
    assert name.family == "Smith"
    assert name.given == "John Jacob"


def test_middle_creator_name():
    creator = {"creatorName": "Smith, John Jacob"}
    name = creator_to_person(creator).name
    assert name.family == "Smith"
    assert name.given == "John Jacob"


def test_name_struct():
    creator = {"familyName": "Smith", "givenName": "John"}
    name = creator_to_person(creator).name
    assert name.family == "Smith"
    assert name.given == "John"


def test_name_struct_overload():
    creator = {"familyName": "Smith", "givenName": "John", "creatorName": "Steve Holt"}
    name = creator_to_person(creator).name
    assert name.family == "Smith"
    assert name.given == "John"


def test_dashed_name():
    creator = {"creatorName": "Hollyhock Manheim-Mannheim-Guerrero-Robinson-Zilberschlag-Hsung-Fonzerelli-McQuack"}
    name = creator_to_person(creator).name
    assert name.family == "Manheim-Mannheim-Guerrero-Robinson-Zilberschlag-Hsung-Fonzerelli-McQuack"
    assert name.given == "Hollyhock"


def test_creator_affiliations():
    creator = {"creatorName": "Kyle Michel", "affiliations": ["Berklee", "NW"]}
    name = creator_to_person(creator).tags == ["Berklee", "NW"]


def test_generate_reference():
    dc = {
        "identifier": {"identifier": "000.000", "identifierType": "DOI"},
        "title": "The joy of the PIF",
        "publisher": "Ether",
        "publicationYear": "2014",
        "creators": [{"creatorName": "Kyle Michel", "affiliations": ["Berklee", "NW"]}]
    }

    ref = datacite_to_pif_reference(dc)
    assert ref.doi == "000.000"
    assert ref.title == "The joy of the PIF"
    assert ref.publisher == "Ether"
    assert ref.year == "2014"
    assert ref.authors[0].given == "Kyle"


def test_add_datacite():
    data_pif = System(properties=[Property(name="Foo", scalars=[Scalar(value="bar")])])
    dc = {
        "identifier": {"identifier": "000.000", "identifierType": "DOI"},
        "title": "The joy of the PIF",
        "publisher": "Ether",
        "publicationYear": "2014",
        "creators": [{"creatorName": "Kyle Michel", "affiliations": ["Berklee", "NW"]}]
    }
    res = add_datacite(data_pif, dc)
    assert res.properties[0].scalars[0].value == "bar"
    assert res.references[0].doi == "000.000" 
