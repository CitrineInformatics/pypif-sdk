from pypif.obj.system import System
from pypif_sdk.util.citrination import set_uids, get_url


def test_set_uids():
    pifs = [System(names=["foo"]), System(names=["bar"])]
    set_uids(pifs)
    for pif in pifs:
        assert pif.uid
    assert len({p.uid for p in pifs}) == 2


def test_explicit_uids():
    pifs = [System(names=["foo"]), System(names=["bar"])]
    uids = ["spam", "eggs"]
    set_uids(pifs, ["spam", "eggs"])
    assert [p.uid for p in pifs] == uids


def test_dup_pifs():
    pifs = [System(names=["foo"]), System(names=["foo"])]
    set_uids(pifs)
    assert len({p.uid for p in pifs}) == 1


def test_get_url():
    pif = System(uid="foobar")
    url = get_url(pif, version=2, dataset=8)
    assert url == "https://citrination.com/datasets/8/version/2/pif/foobar"
