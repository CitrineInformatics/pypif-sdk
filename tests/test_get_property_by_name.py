from pypif_sdk.accessor import get_property_by_name
from pypif.obj import *


def test_get_property_by_name():
    basic_pif = ChemicalSystem(chemical_formula='NaCl', properties=[Property(name='Property 1', scalars=[Scalar(value='10')]), Property(name='Property 2', scalars=[Scalar(value='20')])])

    found_property = get_property_by_name(basic_pif, 'Property 2')

    assert found_property.scalars[0].value == '20'

