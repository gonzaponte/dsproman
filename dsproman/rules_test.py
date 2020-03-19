from pytest import fixture
from pytest import mark

from . database import crystal_types

from . rules import surrounding_peak
from . rules import surrounding_peaks
from . rules import RulesV0
from . rules import RulesV1


@fixture(scope="module", params=range(800, 249, -5))
def ex_wl(request):
    return request.param


@fixture(scope="module", params=(RulesV0, RulesV1))
def rule(request):
    return request.param


@mark.parametrize("step", (1, 5, 10))
def test_surrounding_peak_correct_length(step):
    ex_wl = 300
    delta = 5 * step
    wls = surrounding_peak(ex_wl, delta, step)
    assert len(wls) ==  2 * delta // step + 1


@mark.parametrize("step", (1, 5, 10))
def test_surrounding_peak_borders(step):
    ex_wl = 300
    delta = 5 * step
    wls = surrounding_peak(ex_wl, delta, step)
    assert ex_wl - delta in wls
    assert ex_wl + delta in wls


@mark.parametrize("step", (1, 5, 10))
def test_surrounding_peak_contains_excitation(step):
    ex_wl = 300
    delta = 5 * step
    wls = surrounding_peak(ex_wl, delta, step)
    assert ex_wl in wls


@mark.parametrize("step", (1, 5, 10))
def test_surrounding_peaks_doesnt_contain_duplicates(step):
    ex_wl = 300
    delta = 5 * step
    wls = surrounding_peaks([ex_wl] * 2, delta, step)
    assert sorted(wls) == sorted(surrounding_peak(ex_wl, delta, step))


@mark.parametrize("step", (1, 5, 10))
def test_surrounding_peaks_no_overlap(step):
    ex_wls = 300, 800
    delta  = 5 * step
    wls    = surrounding_peaks(ex_wls, delta, step)

    expected = []
    for ex_wl in ex_wls:
        expected.extend(surrounding_peak(ex_wl, delta, step))

    assert sorted(wls) == sorted(expected)


@mark.parametrize("step", (10, 20))
def test_surrounding_peaks_overlap(step):
    ex_wls = 300, 340
    delta  = 5 * step
    wls    = surrounding_peaks(ex_wls, delta, step)

    expected = []
    for ex_wl in ex_wls:
        expected.extend(surrounding_peak(ex_wl, delta, step))

    assert len(wls) < len(expected)


@mark.parametrize("method", (   "mono_gratings"  ,
                             "spectro_grating"   ,
                             "spectro_wavelength",
                                 "spf_position"  ,
                                 "lpf_position"  ,
                             "flp_exc_position"  ))
def test_rules_base(rule, ex_wl, method):
    assert getattr(rule, method)(ex_wl) is not None


@mark.parametrize("template", ("ambient_template", "background_template", "state_template"))
def test_rules_define_templates(rule, template):
    t = getattr(rule, template)
    assert isinstance(t, str)

    crystal_no = state_no = exposure = grating = 0
    mono_grating = looparound = ex_wl = full_scan = 0
    t.format(**locals())


@mark.parametrize("full_scan", (True, False))
@mark.parametrize("crystal_type", crystal_types)
def test_rules_excitation_wavelengths(rule, full_scan, crystal_type):
    assert len(rule.excitation_wavelengths(full_scan, crystal_type))


@mark.parametrize("full_scan", (True, False))
@mark.parametrize("crystal_type", crystal_types)
def test_rules_excitation_wavelengths_order(rule, full_scan, crystal_type):
    wls = rule.excitation_wavelengths(full_scan, crystal_type)
    for this_wl, next_wl in zip(wls[:-1], wls[1:]):
        assert this_wl > next_wl


def test_rulesv0_exposures():
    assert len(RulesV0.exposures())


@mark.parametrize("crystal_type", crystal_types)
def test_rulesv1_exposures(ex_wl, crystal_type):
    assert len(RulesV1.exposures(ex_wl, crystal_type))


def test_rulesv1_flp_em_pos(ex_wl):
    assert len(RulesV1.flp_em_position(ex_wl))
