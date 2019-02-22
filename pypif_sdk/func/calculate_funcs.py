#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pypif
import re
from pypif.obj import *
import json
import pkg_resources

elements_data = json.loads(
    pkg_resources.resource_string(
        "pypif_sdk.func",
        "elements.json").decode('utf-8'))


def calculate_ideal_atomic_percent(pif):
    """
    Calculates ideal atomic percents from a chemical formula string from a pif. Returns an appended pif with composition elements modified or added.

    :param pif: a ChemicalSystem pif
    :return: modified pif object
    """
    if not isinstance(pif, ChemicalSystem):
        return pif
    if not pif.chemical_formula:
        return pif
    else:
        expanded_formula_no_special_char = _expand_formula_(
            pif.chemical_formula)
        element_array = _create_emprical_compositional_array_(
            expanded_formula_no_special_char)
        appended_e_array = _add_atomic_percents_(element_array)
        for e in appended_e_array:
            # Checks if a Composition element decribing that element already
            # exists.
            if _get_element_in_pif_composition_(pif, e["symbol"]):
                # If it exists, it removes the old Composition object, and
                # inserts a new one with ideal atomic percent added.
                in_pif = _get_element_in_pif_composition_(pif, e["symbol"])
                comp = in_pif[0]
                pif.composition.pop(in_pif[1])
                comp.idealAtomicPercent = e["atomic_percent"]
                pif.composition.append(comp)
            else:
                # If not, it creates a new Composition object with the element
                # and ideal atomic percent.
                comp = Composition()
                comp.element = e["symbol"]
                comp.idealAtomicPercent = e["atomic_percent"]
                pif.composition.append(comp)
        return pif


def calculate_ideal_weight_percent(pif):
    """
    Calculates ideal atomic weight percents from a chemical formula string from a pif. Returns an appended pif with composition elements modified or added.

    :param pif: a ChemicalSystem pif
    :return: modified pif object
    """
    if not isinstance(pif, ChemicalSystem):
        return pif
    if not pif.chemical_formula:
        return pif
    else:
        expanded_formula_no_special_char = _expand_formula_(
            pif.chemical_formula)
        element_array = _create_emprical_compositional_array_(
            expanded_formula_no_special_char)
        appended_e_array = _add_ideal_atomic_weights_(element_array)
        a_array_with_pcts = _add_ideal_weight_percent_(appended_e_array)
        for e in a_array_with_pcts:
            # Checks if a Composition element decribing that element already
            # exists.
            if _get_element_in_pif_composition_(pif, e["symbol"]):
                # If it exists, it removes the old Composition object, and
                # inserts a new one with ideal atomic weight percent added
                in_pif = _get_element_in_pif_composition_(pif, e["symbol"])
                comp = in_pif[0]
                pif.composition.pop(in_pif[1])
                comp.idealWeightPercent = e["weight_percent"]
                pif.composition.append(comp)
            else:
                # If not, it creates a new Composition object with the element
                # and ideal atomic weight percent.
                comp = Composition()
                comp.element = e["symbol"]
                comp.idealWeightPercent = e["weight_percent"]
                pif.composition.append(comp)
        return pif


def _expand_formula_(formula_string):
    """
    Accounts for the many ways a user may write a formula string, and returns an expanded chemical formula string.
    Assumptions:
    -The Chemical Formula string it is supplied is well-written, and has no hanging parethneses
    -The number of repeats occurs after the elemental symbol or ) ] character EXCEPT in the case of a hydrate where it is assumed to be in front of the first element
    -All hydrates explicitly use the · symbol
    -Only (, (,[, ], ., · are "important" symbols to intrepreting the string.
    -IONS ARE NOT HANDLED

    :param formula_string: a messy chemical formula string
    :return: a non-emperical but expanded formula string
    """
    formula_string = re.sub(r'[^A-Za-z0-9\(\)\[\]\·\.]+', '', formula_string)
    hydrate_pos = formula_string.find('·')
    if hydrate_pos >= 0:
        formula_string = _expand_hydrate_(hydrate_pos, formula_string)
    search_result = re.search(
        r'(?:[\(\[]([A-Za-z0-9]+)[\)\]](\d*))',
        formula_string)
    if search_result is None:
        return formula_string
    this_start = search_result.start()
    this_end = search_result.end()
    this_string = search_result.group()
    this_expansion_array = re.findall(
        r'(?:[\(\[]([A-Za-z0-9]+)[\)\]](\d*))', this_string)
    for a in this_expansion_array:
        if a[1] == "":
            a = (a[0], 1)
        parenth_expanded = ""
        multiplier = float(a[1])
        element_array = re.findall('[A-Z][^A-Z]*', a[0])
        for e in element_array:
            occurance_array = re.findall('[0-9][^0-9]*', e)
            if len(occurance_array) == 0:
                occurance_array.append(1)
            for o in occurance_array:
                symbol = re.findall('[A-Z][a-z]*', e)
                total_num = float(o) * multiplier
                if total_num.is_integer():
                    total_num = int(total_num)
                total_str = str(total_num)
                if total_str == "1":
                    total_str = ""
                new_string = symbol[0] + total_str
                parenth_expanded += new_string
        formula_string = formula_string[0:this_start] + \
            parenth_expanded + formula_string[this_end:]
        return _expand_formula_(formula_string)


def _expand_hydrate_(hydrate_pos, formula_string):
    """
    Handles the expansion of hydrate portions of a chemical formula, and expands out the coefficent to all elements

    :param hydrate_pos: the index in the formula_string of the · symbol
    :param formula_string: the unexpanded formula string
    :return: a formula string without the · character with the hydrate portion expanded out
    """
    hydrate = formula_string[hydrate_pos + 1:]
    hydrate_string = ""
    multiplier = float(re.search(r'^[\d\.]+', hydrate).group())
    element_array = re.findall('[A-Z][^A-Z]*', hydrate)
    for e in element_array:
        occurance_array = re.findall('[0-9][^0-9]*', e)
        if len(occurance_array) == 0:
            occurance_array.append(1)
        for o in occurance_array:
            symbol = re.findall('[A-Z][a-z]*', e)
            total_num = float(o) * multiplier
            if total_num.is_integer():
                total_num = int(total_num)
            total_str = str(total_num)
            if total_str == "1":
                total_str = ""
            new_string = symbol[0] + total_str
            hydrate_string += new_string
    return formula_string[:hydrate_pos] + hydrate_string


def _create_compositional_array_(expanded_chemical_formaula_string):
    """
    Splits an expanded chemical formula string into an array of dictionaries containing information about each element

    :param expanded_chemical_formaula_string: a clean (not necessarily emperical, but without any special characters) chemical formula string, as returned by _expand_formula_()
    :return: an array of dictionaries
    """
    element_array = re.findall(
        '[A-Z][^A-Z]*',
        expanded_chemical_formaula_string)
    split_element_array = []
    for s in element_array:
        m = re.match(r"([a-zA-Z]+)([0-9\.]*)", s, re.I)
        if m:
            items = m.groups()
            if items[1] == "":
                items = (items[0], 1)
        this_e = {"symbol": items[0], "occurances": float(items[1])}

        split_element_array.append(this_e)
    return split_element_array


def _consolidate_elemental_array_(elemental_array):
    """
    Accounts for non-empirical chemical formulas by taking in the compositional array generated by _create_compositional_array_() and returning a consolidated array of dictionaries with no repeating elements

    :param elemental_array: an elemental array generated from _create_compositional_array_()
    :return: an array of element dictionaries
    """
    condensed_array = []
    for e in elemental_array:
        exists = False
        for k in condensed_array:
            if k["symbol"] == e["symbol"]:
                exists = True
                k["occurances"] += e["occurances"]
                break
        if not exists:
            condensed_array.append(e)
    return condensed_array


def _calculate_n_atoms_(elemental_array):
    """
    Calculates the total number of atoms in the system.

    :param elemental_array: an array of dictionaries as generated by either _create_compositional_array_() or _consolidate_elemental_array_()
    :return: the total number of atoms (can be a partial number in the case of alloys or partial hydrates)
    """
    return sum(a["occurances"] for a in elemental_array)


def _add_ideal_atomic_weights_(elemental_array):
    """
    Uses elements.json to find the molar mass of the element in question, and then multiplies that by the occurances of the element.
    Adds the "weight" property to each of the dictionaries in elemental_array

    :param elemental_array: an array of dictionaries containing information about the elements in the system
    :return: the appended elemental_array
    """
    for a in elemental_array:
        this_atomic_weight = elements_data[a["symbol"]]["atomic_weight"]
        a["weight"] = a["occurances"] * this_atomic_weight
    return elemental_array


def _calculate_total_mass_(elemental_array):
    """
    Sums the total weight from all the element dictionaries in the elemental_array after each weight has been added (after _add_ideal_atomic_weights_())

    :param elemental_array: an array of dictionaries containing information about the elements in the system
    :return: the total weight of the system
    """
    return sum(a["weight"] for a in elemental_array)


def _add_ideal_weight_percent_(elemental_array):
    """
    Adds the "weight_percent" property to each of the dictionaries in elemental_array

    :param elemental_array: an array of dictionaries containing information about the elements in the system
    :return: the appended elemental_array
    """
    t_mass = _calculate_total_mass_(elemental_array)
    for a in elemental_array:
        a["weight_percent"] = a["weight"] / t_mass * 100
    return elemental_array


def _create_emprical_compositional_array_(expanded_chemical_formaula_string):
    """
    Turns a chemical formula into an array of objects with element names and their corresponding number of occurances

    :param expanded_chemical_formaula_string: chemical formula string that is expanded and has no special characters
    :return: an elemental_array (array of dictionaries) containing information on each element in the system and it's total number of occurances (no duplicates)
    """
    elemental_array = _create_compositional_array_(
        expanded_chemical_formaula_string)
    condensed_array = _consolidate_elemental_array_(elemental_array)
    return condensed_array


def _add_atomic_percents_(elemental_array):
    """
    Adds ideal atomic percents to a emperical compositional element array generated using _create_emprical_compositional_array_()

    :param elemental_array: an array of dictionaries containing information about the elements in the system
    :return: the elemental_array with the atomic percent of each element added
    """
    n_atoms = _calculate_n_atoms_(elemental_array)
    for e in elemental_array:
        e["atomic_percent"] = e["occurances"] / n_atoms * 100
    return elemental_array


def _get_element_in_pif_composition_(pif, elemental_symbol):
    """
    If the element in question if in the composition array in the pif, it returns that Composition object and the position in the composition array otherwise it returns False

    :param pif: ChemicalSystem Pif in question
    :param elemental_symbol: string of the atomic symbol of the element in question
    :return: either False if not found in the composition or the Compositional object along with its index in the composition array in the pif
    """
    if pif.composition is None:
        pif.composition = []
    for i, c in enumerate(pif.composition):
        if c.element == elemental_symbol or c.element.lower(
        ) == elements_data[elemental_symbol]["name"].lower():
            return [c, i]
        i += 1
    return False
