from pypif.obj.common import Property, Scalar, Person, Name, License, Reference, Value
from pypif.obj.system import System, ChemicalSystem
from pypif.obj.system.chemical.common import Composition
from citrination_client import DatasetSearchHit
from pypif_sdk.interop.mdf import _to_user_defined, _construct_new_key, _to_meta_data
from pypif_sdk.interop.mdf import query_to_mdf_records

import pytest
from os import environ
import json


test_pif1 = ChemicalSystem(
    uid="0",
    chemical_formula="CH4",
    names = ["methane", "natural gas"],
    contacts = [Person(name=Name(given="Albert", family="Einstein"), orcid="123456"), Person(name=Name(given="Adam", family="Min"), email="admin@citrine.io")],
    references = [Reference(doi="doi", authors=[Name(given="Captain", family="Marvel")])],
    licenses = [License(url="url")],
    tags = ["too long", "didn't read"],
    properties = [
        Property(name="foo", scalars=[Scalar(value="bar")]),
        Property(name="spam", scalrs=[Scalar(value="eggs")])
    ]
)
test_pif2 = ChemicalSystem(
    uid="0",
    composition=[Composition(element="H"), Composition(element="S"), Composition(element="O")],
    references=[]
    )


@pytest.mark.skipif("CITRINATION_API_KEY" not in environ, reason="No API key available")
def test_query_to_mdf_records():
    """Big integration test to make sure everything is working"""
    records = query_to_mdf_records(dataset_id=153258, acl=["public"])

    assert len(records) == 9, "Some records were not converted"

    assert all("mdf" in r for r in records), "Records are majorly malformed"
    for r in records:
        rd = json.loads(r)
        source_name = next(x for x in rd.keys() if x != "mdf")
        user_block = rd[source_name]
        assert "Density_kg_m_3" in user_block, "Failed to convert property"
        assert "Heat_treatment" in user_block, "Failed to convert process step detail"


def test_property_value():
    """Test that a simple property gets pulled out"""
    sys = System(properties=[Property(name="foo", scalars=[Scalar(value="bar")])])
    user_data = _to_user_defined(sys)
    assert user_data["foo"] == "bar"
   
 
def test_property_list():
    """Test that a property with a list of scalars gets pulled out"""
    sys = System(properties=[Property(name="foo", scalars=[Scalar(value="spam"), Scalar(value="eggs")])])
    user_data = _to_user_defined(sys)
    assert user_data["foo"] == ["spam", "eggs"] 


def test_property_vector():
    """Test that a vector gets pulled out"""
    sys = System(properties=[Property(name="foo", units="bar", vectors=[[Scalar(value="spam"), Scalar(value="eggs")]])])
    user_data = _to_user_defined(sys)
    assert user_data["foo_bar"] == ["spam", "eggs"] 


def test_condition():
    """Test that conditions are flattened and added"""
    condition = Value(name="spam", scalars=[Scalar(value="eggs")])
    sys = System(properties=[
        Property(name="foo", scalars=[Scalar(value="bar")], conditions=[condition])
    ])
    user_data = _to_user_defined(sys)
    assert user_data["spam"] == "eggs"


def test_construct_new_key():
    """Test the new key constructions"""
    assert _construct_new_key("foo") == "foo"
    assert _construct_new_key("foo", units="bar") == "foo_bar"
    assert _construct_new_key("foo bar") == "foo_bar"
    assert _construct_new_key("#foo", units="g/cm^3") == "_foo_g_cm_3"


def test_to_meta_data():
    dataset_info = DatasetSearchHit(
        name="A dataset",
        id=0,
        owner="Albert Einstein",
        email="al@rel.gr"
    )
    meta_data1 = _to_meta_data(test_pif1, dataset_info, acl=["public"])
    assert meta_data1 == {
        "title": "methane",
        "composition": "CH4",
        "acl": ["public"],
        "source_name": "A_dataset",
        "data_contact": [{
            "given_name": "Albert",
            "family_name": "Einstein",
            "orcid": "123456"
            },{
            "given_name": "Adam",
            "family_name": "Min",
            "email": "admin@citrine.io"
            }],
        "data_contributor": [{
            "given_name": "Albert", 
            "family_name": "Einstein",
            "email": "al@rel.gr"
        }],
        "citation": ["doi"],
        "author": [{
            "given_name": "Captain",
            "family_name": "Marvel"
            }],
        "license": "url",
        "tags": ["too long", "didn't read"],
        "links": {
            "landing_page" : "https://citrination.com/datasets/0",
            "publication": ["doi"]
            }
        }
    dataset_info.owner = None
    meta_data2 = _to_meta_data(test_pif2, dataset_info, acl=["public"])
    assert meta_data2 == {
        "title": "Citrine PIF 0",
        "composition": "HSO",
        "acl": ["public"],
        "source_name": "A_dataset",
        "data_contributor": [{}],
        "links": {
            "landing_page": "https://citrination.com/datasets/0"
            }
        }

