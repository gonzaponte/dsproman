from itertools import chain

from . database import crystal_types
from . database import excitations


def surrounding_peak(ex_wl, delta, step=10):
    return tuple(range(ex_wl + delta, ex_wl - delta - 1, -step))

def surrounding_peaks(ex_wls, delta, step=10):
    peaks = (surrounding_peak(ex_wl, delta, step) for ex_wl in ex_wls)
    peaks = set(chain.from_iterable(peaks))
    return list(peaks)


class Rules:
    def mono_gratings(ex_wl):
        return (2,) if ex_wl >= 400 else (1, 2)

    def spectro_grating(ex_wl):
        return 2 if ex_wl >= 400 else 1


class RulesV0(Rules):
    ambient_template    = "ambient_crystal_{crystal_no}_exposure_100"
    background_template = "background_crystal_{crystal_no}_exposure_100"
    state_template      = "state_{state_no}_crystal_{crystal_no}_ex_wl_{ex_wl}_exposure_{exposure}_grating_{grating}_looparound_{looparound}"

    def spf_position(ex_wl):
        if 390 <= ex_wl < 440: return 1
        if 440 <= ex_wl < 490: return 2
        if 490 <= ex_wl < 540: return 3
        if 540 <= ex_wl < 590: return 4
        if 590 <= ex_wl < 640: return 5
        return 6


    def lpf_position(ex_wl):
        if 350 <= ex_wl < 400: return 1
        if 400 <= ex_wl < 450: return 2
        if 450 <= ex_wl < 500: return 3
        if 500 <= ex_wl < 550: return 4
        if 550 <= ex_wl < 600: return 5
        return 6

    def flp_exc_position(ex_wl):
        return "up" if ex_wl >= 360 else "down"

    def excitation_wavelengths(full_scan, crystal_type):
        if full_scan:
            exwls = surrounding_peaks(excitations[crystal_type], 20, 5)
        else:
            exwls = sorted(set(excitations[crystal_type]), reverse=True)
        return sorted(exwls, reverse=True)

    def spectro_wavelength(ex_wl):
        return ex_wl + 420 + 10

    def exposures():
        return (0.1, 1, 10) + (0.1,) * 4 + (1,) * 4 + (10,)


class RulesV1(Rules):
    ambient_template    = "ambient_crystal_{crystal_no}_fullscan_{full_scan}_exposure_100"
    background_template = "background_crystal_{crystal_no}_fullscan_{full_scan}_exposure_100"
    baseline_template   = "baseline_crystal_{crystal_no}_fullscan_{full_scan}"
    state_template      = "state_{state_no}_crystal_{crystal_no}_fullscan_{full_scan}_exwl_{ex_wl}_monograting_{mono_grating}_exposure_{exposure}"

    def spf_position(ex_wl):
        if 390 <= ex_wl < 440: return 1
        if 440 <= ex_wl < 490: return 2
        if 490 <= ex_wl < 540: return 3
        if 540 <= ex_wl < 590: return 4
        if 590 <= ex_wl < 640: return 5
        return 6


    def lpf_position(ex_wl):
        if 350 <= ex_wl < 400: return 1
        if 400 <= ex_wl < 450: return 2
        if 450 <= ex_wl < 500: return 3
        if 500 <= ex_wl < 550: return 4
        if 550 <= ex_wl      : return 5
        if 250 <= ex_wl < 350: return 6
        print(f"WARNING: No LPFW rule set for excitation wavelength {ex_wl}")

    def flp_exc_position(ex_wl):
        return "up" if ex_wl >= 450 else "down"

    def flp_em_position(ex_wl):
        return "up" if ex_wl >= 300 else "down"

    def excitation_wavelengths(full_scan, crystal_type=None):
        if full_scan:
            return tuple(range(800, 249, -10))
        elif crystal_type in crystal_types:
            return sorted(set(excitations[crystal_type]), reverse=True)
        else:
            raise ValueError(f"Attempted to get specific wavelengths for unknown crystal type {crystal_type}")

    def spectro_wavelength(ex_wl):
        return ex_wl + 420 + 25

    def exposures(ex_wl=None, crystal_type=None):
        e = 0.2, 2, 10
        if ex_wl is not None and crystal_type is not None and ex_wl in excitations[crystal_type]:
            e = e + (0.2,) * 5 + (2,) * 5

        return e


class RulesV2(RulesV1):
    def mono_gratings(ex_wl):
        return (1,) if ex_wl < 400 else (2, 1) if ex_wl == 400 else (2,)

    def flp_em_position(ex_wl):
        return "up" if ex_wl >= 250 else "down"
