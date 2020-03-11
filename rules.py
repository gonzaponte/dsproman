
class RulesV0:
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


class RulesV1:
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
