from pypif_sdk.func import replace_by_key, copy
from pypif_sdk.accessor import get_property_by_name
from pypif.obj import System, Property, Scalar, Value, FileReference


test_pif = System(
    names=["methane"],
    properties=[
        Property(name="foo", scalars=[Scalar(value="bar")]),
        Property(
            name="spam",
            units="eV",
            scalars=[Scalar(value=2.7)],
            conditions=[Value(name="tomato", units="eV", scalars=[Scalar(value=1.0)])]
        ),
        Property(
            name="image",
            files=[FileReference(relative_path="/tmp/file.png")]
        )
    ]
)


def test_simple_replace():
    """Test replace a single field with default arguments"""
    prop = get_property_by_name(copy(test_pif), "image")
    assert prop.files[0].relative_path == "/tmp/file.png", "Didn't shorten file name"
    new_pif = replace_by_key(test_pif, "relative_path", {"/tmp/file.png": "file.png"})
    prop = get_propety_by_name(new_pif, "image")
    assert prop.files[0].relative_path == "file.png", "Didn't shorten file name"
    assert prop.files[0].relative_path == "file.png", "Didn't shorten file name"


def test_multi_replace():
    """Test that keys are replaced at two levels"""
    new_pif = replace_by_key(test_pif, "units", {"eV": "erg"})
    prop = next(x for x in new_pif.properties if x.name == "spam")
    assert prop.units == "erg", "Didn't replace units in property"
    assert prop.conditions[0].units == "erg", "Didn't replace units in condition"


def test_new_key():
    new_pif = replace_by_key(test_pif, "relative_path", {"/tmp/file.png": "www.file.png"}, new_key="url", remove=True)
    prop = get_property_by_name(new_pif, "image")
    assert prop.files[0].url == "www.file.png", "Didn't set URL"
    assert prop.files[0].relative_path is None, "Didn't remove relative_path"
