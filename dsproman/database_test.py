from pytest import mark

from . database import crystal_types
from . database import signals
from . database import excitations
from . database import emissions


def test_signals_are_iteratable():
    for crystal in signals.values():
        assert len(crystal) >= 1
        for emissions in crystal:
            assert len(emissions) == 2


@mark.parametrize("data", (excitations, emissions))
def test_excitations_emissions_are_iteratable(data):
    for crystal in data.values():
        assert len(crystal) >= 1
        for emission in crystal:
            assert isinstance(emission, int)


@mark.parametrize("data", (signals, excitations, emissions))
def test_data_contains_all_crystals(data):
    for crystal in crystal_types:
        assert crystal in data
