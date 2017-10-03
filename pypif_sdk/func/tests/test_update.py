from pypif_sdk.func import update
from pypif.obj import System, Property, Scalar


test_pif = System(
    properties=[
        Property(name="foo", scalars=[Scalar(value="bar")]),
        Property(name="spam", scalars=[Scalar(value=2.7)]),
    ]
)


def test_update_no_conflicts():
    """Test that update works when there are no conflicts"""
    no_conflict_pif = System(
        names=["gas", "methane"]
    )
    combined = update(test_pif, no_conflict_pif)
    expected = {"foo": "bar", "spam": 2.7}

    assert set(x.name for x in combined.properties) == set(expected.keys())
    assert set(x.scalars[0].value for x in combined.properties) == set(expected.values())
    for prop in combined.properties:
        assert expected[prop.name] == prop.scalars[0].value

    assert combined.names == ["gas", "methane"]


def test_update_conflict():
    """Test that update works when not extending and a field is redefined"""
    more_pif = System(
        properties=[
            Property(name="band gap", scalars=[Scalar(value=1.3)]),
            Property(name="phase", scalars=[Scalar(value="gas")]),
        ]
    )
    combined = update(test_pif, more_pif)
    expected = {"band gap": 1.3, "phase": "gas"}

    assert set(x.name for x in combined.properties) == set(expected.keys())
    assert set(x.scalars[0].value for x in combined.properties) == set(expected.values())
    for prop in combined.properties:
        assert expected[prop.name] == prop.scalars[0].value


def test_update_extend():
    """Test that update works when extending with no dups"""
    more_pif = System(
        properties=[
            Property(name="band gap", scalars=[Scalar(value=1.3)]),
            Property(name="phase", scalars=[Scalar(value="gas")]),
        ]
    )
    combined = update(test_pif, more_pif, extend=True)
    expected = {"band gap": 1.3, "phase": "gas", "foo": "bar", "spam": 2.7}

    assert set(x.name for x in combined.properties) == set(expected.keys())
    assert set(x.scalars[0].value for x in combined.properties) == set(expected.values())
    for prop in combined.properties:
        assert expected[prop.name] == prop.scalars[0].value


def test_update_conflicts():
    """Test that update works when there are conflicts"""
    conflict_pif = System(
        properties=[
            Property(name="band gap", scalars=[Scalar(value=1.3)]),
            Property(name="phase", scalars=[Scalar(value="gas")]),
            Property(name="spam", scalars=[Scalar(value=2.0)]),
        ]
    )

    combined = update(test_pif, conflict_pif, extend=True)
    expected = {"band gap": 1.3, "phase": "gas", "foo": "bar", "spam": 2.0}

    assert set(x.name for x in combined.properties) == set(expected.keys())
    assert set(x.scalars[0].value for x in combined.properties) == set(expected.values())
    for prop in combined.properties:
        assert expected[prop.name] == prop.scalars[0].value
