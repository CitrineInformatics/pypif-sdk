# pypif-sdk
![status](https://travis-ci.org/CitrineInformatics/pypif-sdk.svg?branch=master)
![PyPI version](https://badge.fury.io/py/pypif-sdk.svg)

Tools for working with PIF objects that go beyond the low level objects defined in [pypif](https://github.com/CitrineInformatics/pypif).

## Functionz

Functional components that do useful things like replace fields, update or merge pairs of PIFs, and create deep copies.

## Accessors

Accessors functions that return PIF objects nested within a PIF and can index by name rather than position.

## ReadViews

A dictionary-like read-only view into a PIF that indexes members by name and elevates keys up the PIF hierarchy as long as they are unambiguous.

## Interoperability

Functions to export a PIF into an external data format.
Currently supported formats are:
 - MDF record metadata
