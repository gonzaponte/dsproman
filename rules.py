from itertools import chain

from . database import excitations


def surrounding_peak(ex_wl, delta, step=10):
    return list(range(ex_wl - delta, ex_wl + delta + 1, step))

def surrounding_peaks(ex_wls, delta, step=10):
    peaks = (surrounding_peak(ex_wl, delta, step) for ex_wl in ex_wls)
    peaks = set(chain.from_iterable(peaks))
    return sorted(peaks, reverse=True)


class Rules:
    def mono_gratings(ex_wl):
        return (2,) if ex_wl >= 400 else (1, 2)

    def spectro_grating(ex_wl):
        return 2 if ex_wl >= 400 else 1


class RulesV0(Rules):

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
            return surrounding_peaks(excitations[crystal_type], 20, 5)
        else:
            return excitations[crystal_type]

    def spectro_wavelength(ex_wl):
        return ex_wl + 420 + 10

    def exposures():
        return (0.1, 1, 10) + (0.1,) * 5 + (1,) * 5


class RulesV1(Rules):

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
        if 250 <= ex_wl < 300: return 6
        print(f"WARNING: No LPFW rule set for excitation wavelength {ex_wl}")

    def flp_exc_position(ex_wl):
        return "up" if ex_wl >= 450 else "down"

    def flp_emm_position(ex_wl):
        return "up" if ex_wl >= 300 else "down"

    def excitation_wavelengths(full_scan, crystal_type):
        if full_scan:
            return tuple(range(800, 249, 10))
        else:
            return excitations[crystal_type]

    def spectro_wavelength(ex_wl):
        return ex_wl + 420 + 25

    def exposures(ex_wl, crystal_type):
        e = 0.2, 2, 10
        if ex_wl in excitations[crystal_type]:
            e = e + (0.2,) * 5 + (2,) * 5

        return e
