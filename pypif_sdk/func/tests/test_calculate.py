#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pypif_sdk.func import *
from pypif_sdk.func.calculate_funcs import _expand_formula_, _expand_hydrate_, _create_compositional_array_, _consolidate_elemental_array_, _calculate_n_atoms_, _add_ideal_atomic_weights_, _add_ideal_weight_percent_, _create_emprical_compositional_array_, _add_atomic_percents_, _get_element_in_pif_composition_
from pypif.obj import *
import json

test_pif_one = ChemicalSystem(
    names=["nonanal"],
    chemical_formula="C9H18O",
    properties=[Property(name="foo", scalars=[Scalar(value="bar")])]
)
test_pif_two = ChemicalSystem(
    names=["nonanal"],
    chemical_formula="C6H10OC3H8",
    properties=[Property(name="foo", scalars=[Scalar(value="bar")])]
)
test_pif_three = ChemicalSystem(
    names=["parenth nonanal"],
    chemical_formula="CH3(CH2)7OHC",
    properties=[Property(name="foo", scalars=[Scalar(value="bar")])]
)

test_pif_four = ChemicalSystem(
    names=["copper(II) nitrate trihydrate"],
    chemical_formula="Cu(NO3)2 · 3H2O",
    properties=[Property(name="foo", scalars=[Scalar(value="bar")])]
)

test_pif_five = ChemicalSystem(
    names=["ammonium hexathiocyanoplatinate(IV)"],
    chemical_formula="(NH4)2[Pt(SCN)6]",
    properties=[Property(name="foo", scalars=[Scalar(value="bar")])]
)
test_pif_six = ChemicalSystem(
    names=["ammonium hexathiocyanoplatinate(IV)"],
    chemical_formula="(NH$_{4}$)$_{2}$[Pt(SCN)$_6$]",
    properties=[Property(name="foo", scalars=[Scalar(value="bar")])]
)
test_pif_seven = ChemicalSystem(
    names=["calcium sulfate hemihydrate"],
    chemical_formula="CaSO4·0.5H2O",
    properties=[Property(name="foo", scalars=[Scalar(value="bar")])]
)
test_pif_eight = ChemicalSystem(
    names=["Zr glass"],
    chemical_formula="Zr46.75Ti8.25Cu7.5Ni10Be27.5",
    properties=[Property(name="foo", scalars=[Scalar(value="bar")])]
)

test_pif_nine = ChemicalSystem(
    names=["Zr glass"],
    chemical_formula="Zr46.75Ti8.25Cu7.5Ni10Be27.5",
    properties=[Property(name="foo", scalars=[Scalar(value="bar")])],
    composition=[Composition(element="Zirconium")]
)


def test_calculate_ideal_atomic_percent():
    """
    Tests that calculate_ideal_atomic_percent() works under a variety of circumstances
    """
    pif_one = calculate_ideal_atomic_percent(test_pif_one)
    assert round(pif_one.composition[0].idealAtomicPercent, 2) == 32.14
    assert round(pif_one.composition[1].idealAtomicPercent, 2) == 64.29
    assert round(pif_one.composition[2].idealAtomicPercent, 2) == 3.57
    pif_two = calculate_ideal_atomic_percent(test_pif_two)
    assert len(pif_two.composition) == 3
    assert round(pif_two.composition[0].idealAtomicPercent, 2) == 32.14
    assert round(pif_two.composition[1].idealAtomicPercent, 2) == 64.29
    assert round(pif_two.composition[2].idealAtomicPercent, 2) == 3.57
    pif_three = calculate_ideal_atomic_percent(test_pif_three)
    assert len(pif_three.composition) == 3
    assert round(pif_three.composition[0].idealAtomicPercent, 2) == 32.14
    assert round(pif_three.composition[1].idealAtomicPercent, 2) == 64.29
    assert round(pif_three.composition[2].idealAtomicPercent, 2) == 3.57
    pif_four = calculate_ideal_atomic_percent(test_pif_four)
    assert len(pif_four.composition) == 4
    assert round(pif_four.composition[0].idealAtomicPercent, 2) == 5.56
    assert round(pif_four.composition[1].idealAtomicPercent, 2) == 11.11
    assert round(pif_four.composition[2].idealAtomicPercent, 2) == 50.00
    assert round(pif_four.composition[3].idealAtomicPercent, 2) == 33.33
    pif_five = calculate_ideal_atomic_percent(test_pif_five)
    assert len(pif_five.composition) == 5
    assert round(pif_five.composition[0].idealAtomicPercent, 2) == 27.59
    assert round(pif_five.composition[1].idealAtomicPercent, 2) == 27.59
    assert round(pif_five.composition[2].idealAtomicPercent, 2) == 3.45
    assert round(pif_five.composition[3].idealAtomicPercent, 2) == 20.69
    assert round(pif_five.composition[4].idealAtomicPercent, 2) == 20.69
    pif_six = calculate_ideal_atomic_percent(test_pif_six)
    assert len(pif_six.composition) == 5
    assert round(pif_six.composition[0].idealAtomicPercent, 2) == 27.59
    assert round(pif_six.composition[1].idealAtomicPercent, 2) == 27.59
    assert round(pif_six.composition[2].idealAtomicPercent, 2) == 3.45
    assert round(pif_six.composition[3].idealAtomicPercent, 2) == 20.69
    assert round(pif_six.composition[4].idealAtomicPercent, 2) == 20.69
    pif_seven = calculate_ideal_atomic_percent(test_pif_seven)
    assert len(pif_seven.composition) == 4
    assert round(pif_seven.composition[0].idealAtomicPercent, 2) == 13.33
    assert round(pif_seven.composition[1].idealAtomicPercent, 2) == 13.33
    assert round(pif_seven.composition[2].idealAtomicPercent, 2) == 60.00
    assert round(pif_seven.composition[3].idealAtomicPercent, 2) == 13.33
    pif_eight = calculate_ideal_atomic_percent(test_pif_eight)
    assert len(pif_eight.composition) == 5
    assert round(pif_eight.composition[0].idealAtomicPercent, 2) == 46.75
    assert round(pif_eight.composition[1].idealAtomicPercent, 2) == 8.25
    assert round(pif_eight.composition[2].idealAtomicPercent, 2) == 7.5
    assert round(pif_eight.composition[3].idealAtomicPercent, 2) == 10
    assert round(pif_eight.composition[4].idealAtomicPercent, 2) == 27.5


def test_calculate_ideal_weight_percent():
    """
    Tests that calculate_ideal_weight_percent() works under a variety of circumstances
    """
    pif_one = calculate_ideal_weight_percent(test_pif_one)

    assert len(pif_one.composition) == 3
    assert round(pif_one.composition[0].idealWeightPercent, 2) == 76.00
    assert round(pif_one.composition[1].idealWeightPercent, 2) == 12.76
    assert round(pif_one.composition[2].idealWeightPercent, 2) == 11.25
    pif_two = calculate_ideal_weight_percent(test_pif_two)
    assert len(pif_two.composition) == 3
    assert round(pif_two.composition[0].idealWeightPercent, 2) == 76.00
    assert round(pif_two.composition[1].idealWeightPercent, 2) == 12.76
    assert round(pif_two.composition[2].idealWeightPercent, 2) == 11.25
    pif_three = calculate_ideal_weight_percent(test_pif_three)
    assert len(pif_three.composition) == 3
    assert round(pif_three.composition[0].idealWeightPercent, 2) == 76.00
    assert round(pif_three.composition[1].idealWeightPercent, 2) == 12.76
    assert round(pif_three.composition[2].idealWeightPercent, 2) == 11.25
    pif_four = calculate_ideal_weight_percent(test_pif_four)
    assert len(pif_four.composition) == 4
    assert round(pif_four.composition[0].idealWeightPercent, 2) == 26.30
    assert round(pif_four.composition[1].idealWeightPercent, 2) == 11.60
    assert round(pif_four.composition[2].idealWeightPercent, 2) == 59.60
    assert round(pif_four.composition[3].idealWeightPercent, 2) == 2.50
    pif_five = calculate_ideal_weight_percent(test_pif_five)
    assert len(pif_five.composition) == 5
    assert round(pif_five.composition[0].idealWeightPercent, 2) == 19.33
    assert round(pif_five.composition[1].idealWeightPercent, 2) == 1.39
    assert round(pif_five.composition[2].idealWeightPercent, 2) == 33.66
    assert round(pif_five.composition[3].idealWeightPercent, 2) == 33.19
    assert round(pif_five.composition[4].idealWeightPercent, 2) == 12.43
    pif_six = calculate_ideal_weight_percent(test_pif_six)
    assert len(pif_six.composition) == 5
    assert round(pif_six.composition[0].idealWeightPercent, 2) == 19.33
    assert round(pif_six.composition[1].idealWeightPercent, 2) == 1.39
    assert round(pif_six.composition[2].idealWeightPercent, 2) == 33.66
    assert round(pif_six.composition[3].idealWeightPercent, 2) == 33.19
    assert round(pif_six.composition[4].idealWeightPercent, 2) == 12.43
    pif_seven = calculate_ideal_weight_percent(test_pif_seven)
    assert len(pif_seven.composition) == 4
    assert round(pif_seven.composition[0].idealWeightPercent, 2) == 27.61
    assert round(pif_seven.composition[1].idealWeightPercent, 2) == 22.09
    assert round(pif_seven.composition[2].idealWeightPercent, 2) == 49.60
    assert round(pif_seven.composition[3].idealWeightPercent, 2) == 0.69
    pif_eight = calculate_ideal_weight_percent(test_pif_eight)
    assert len(pif_eight.composition) == 5
    assert round(pif_eight.composition[0].idealWeightPercent, 2) == 71.42
    assert round(pif_eight.composition[1].idealWeightPercent, 2) == 6.61
    assert round(pif_eight.composition[2].idealWeightPercent, 2) == 7.98
    assert round(pif_eight.composition[3].idealWeightPercent, 2) == 9.83
    assert round(pif_eight.composition[4].idealWeightPercent, 2) == 4.15


def test_expand_formula_():
    """
    Tests _expand_formula_() to ensure complex parentheses are handled correctly
    """
    assert _expand_formula_("(NH4)2[Pt(SCN)6]") == "N2H8PtS6C6N6"


def test_expand_hydrate_():
    """
    Tests _expand_hydrate_() to ensure hydrate chemical formulas can be properly expanded even with decimal values
    """
    assert _expand_hydrate_(5, "CaSO4·0.5H2O") == "CaSO4HO0.5"


def test_create_compositional_array_():
    """
    Tests that _create_compositional_array_() returns an array of compositions for both whole number and decimal values
    """
    assert _create_compositional_array_("N2H8PtS6C6N6") == [
        {"symbol": "N", "occurances": 2},
        {"symbol": "H", "occurances": 8},
        {"symbol": "Pt", "occurances": 1},
        {"symbol": "S", "occurances": 6},
        {"symbol": "C", "occurances": 6},
        {"symbol": "N", "occurances": 6}]

    assert _create_compositional_array_("CaSO4HO0.5") == [
        {"symbol": "Ca", "occurances": 1},
        {"symbol": "S", "occurances": 1},
        {"symbol": "O", "occurances": 4},
        {"symbol": "H", "occurances": 1},
        {"symbol": "O", "occurances": 0.5}
    ]


def test_consolidate_elemental_array_():
    """
    Tests that _consolidate_elemental_array_() returns a consolidates array of compositions for both whole number and decimal values
    """
    input_array = [
        {"symbol": "N", "occurances": 2},
        {"symbol": "H", "occurances": 8},
        {"symbol": "Pt", "occurances": 1},
        {"symbol": "S", "occurances": 6},
        {"symbol": "C", "occurances": 6},
        {"symbol": "N", "occurances": 6},
        {"symbol": "C", "occurances": 2}
    ]
    output_array = [
        {"symbol": "N", "occurances": 8},
        {"symbol": "H", "occurances": 8},
        {"symbol": "Pt", "occurances": 1},
        {"symbol": "S", "occurances": 6},
        {"symbol": "C", "occurances": 8}
    ]
    input_array_dec = [
        {"symbol": "Ca", "occurances": 1},
        {"symbol": "S", "occurances": 1},
        {"symbol": "O", "occurances": 4},
        {"symbol": "H", "occurances": 1},
        {"symbol": "O", "occurances": 0.5}
    ]
    output_array_dec = [
        {"symbol": "Ca", "occurances": 1},
        {"symbol": "S", "occurances": 1},
        {"symbol": "O", "occurances": 4.5},
        {"symbol": "H", "occurances": 1}
    ]
    assert _consolidate_elemental_array_(input_array) == output_array
    assert _consolidate_elemental_array_(input_array_dec) == output_array_dec


def test_calculate_n_atoms_():
    """
    Tests that _calculate_n_atoms_ returns the correct value for both whole number and decimal values
    """
    assert _calculate_n_atoms_([
        {"symbol": "Ca", "occurances": 1},
        {"symbol": "S", "occurances": 1},
        {"symbol": "O", "occurances": 4},
        {"symbol": "H", "occurances": 1},
        {"symbol": "O", "occurances": 0.5}
    ]) == 7.5


def test_add_ideal_atomic_weights_():
    """
    Tests that _add_ideal_atomic_weights_() returns a modified array
    """
    input_array = [
        {"symbol": "N", "occurances": 8},
        {"symbol": "H", "occurances": 8},
        {"symbol": "Pt", "occurances": 1},
        {"symbol": "S", "occurances": 6},
        {"symbol": "C", "occurances": 8}
    ]
    output_array = [
        {"symbol": "N", "occurances": 8, "weight": 14.007 * 8},
        {"symbol": "H", "occurances": 8, "weight": 1.008 * 8},
        {"symbol": "Pt", "occurances": 1, "weight": 195.084},
        {"symbol": "S", "occurances": 6, "weight": 32.06 * 6},
        {"symbol": "C", "occurances": 8, "weight": 12.011 * 8}
    ]
    assert _add_ideal_atomic_weights_(input_array) == output_array


def test_add_ideal_weight_percent_():
    """
    Tests that _add_ideal_weight_percent_() returns a modified array
    """
    input_array = [
        {"symbol": "N", "occurances": 8, "weight": 14.007 * 8},
        {"symbol": "H", "occurances": 8, "weight": 1.008 * 8},
        {"symbol": "Pt", "occurances": 1, "weight": 195.084},
        {"symbol": "S", "occurances": 6, "weight": 32.06 * 6},
        {"symbol": "C", "occurances": 8, "weight": 12.011 * 8}
    ]
    output_array = [
        {"symbol": "N", "occurances": 8, "weight": 14.007 * 8, 
            "weight_percent": 14.007 * 8 / 603.652 * 100},
        {"symbol": "H", "occurances": 8, "weight": 1.008 * 8, 
            "weight_percent": 1.008 * 8 / 603.652 * 100},
        {"symbol": "Pt", "occurances": 1, "weight": 195.084,
            "weight_percent": 195.084 / 603.652 * 100},
        {"symbol": "S", "occurances": 6, "weight": 32.06 * 6,
            "weight_percent": 32.06 * 6 / 603.652 * 100},
        {"symbol": "C", "occurances": 8, "weight": 12.011 * 8,
            "weight_percent": 12.011 * 8 / 603.652 * 100}
    ]
    assert _add_ideal_weight_percent_(input_array) == output_array


def test_create_emprical_compositional_array_():
    """
    Tests that _create_emprical_compositional_array_() returns an emperical array of elements
    """
    assert _create_emprical_compositional_array_("CaSO4HO0.5") == [
        {"symbol": "Ca", "occurances": 1},
        {"symbol": "S", "occurances": 1},
        {"symbol": "O", "occurances": 4.5},
        {"symbol": "H", "occurances": 1}
    ]


def test_add_atomic_percents_():
    """
    Tests that _add_atomic_percents_() returns a modified array
    """
    input_array = [
        {"symbol": "N", "occurances": 8},
        {"symbol": "H", "occurances": 8},
        {"symbol": "Pt", "occurances": 1},
        {"symbol": "S", "occurances": 6},
        {"symbol": "C", "occurances": 8}
    ]
    output_array = [
        {"symbol": "N", "occurances": 8, "atomic_percent": 8 / 31 * 100},
        {"symbol": "H", "occurances": 8, "atomic_percent": 8 / 31 * 100},
        {"symbol": "Pt", "occurances": 1, "atomic_percent": 1 / 31 * 100},
        {"symbol": "S", "occurances": 6, "atomic_percent": 6 / 31 * 100},
        {"symbol": "C", "occurances": 8, "atomic_percent": 8 / 31 * 100}
    ]
    assert _add_atomic_percents_(input_array) == output_array


def test_get_element_in_pif_composition_():
    """
    tests that _check_if_element_exists_in_pif_composition_() can check for both element names and element symbols
    """
    assert _get_element_in_pif_composition_(test_pif_eight, "Ca") == False
    correct_comp = Composition(element="Zirconium")
    assert dumps(_get_element_in_pif_composition_(
        test_pif_nine, "Zr")) == dumps([correct_comp, 0])
