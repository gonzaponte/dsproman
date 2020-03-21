from . utils import temporary


def initialize(s):
    s.source        .power      = 100
    s.source_shutter.control    = "camera"
    s.spectro       .shutter    = "auto"
    s.spectro       .slit_width = 1000


def take_data(s, filename, state_no=None):
    s.spectro    .save_path = f"{filename}_signal.asc"
    s.power_meter.save_path = f"{filename}_power.asc"

    s.add_database_entry(state_no)
    with temporary(s, "power_meter", "recording", True):
        s.spectro.running   = True

    s.spectro    .saved     = True
    s.power_meter.saved     = True


def take_ambient(s, filename):
    with temporary(s, "source_shutter", "control", "computer"):
        s.source_shutter.on         = False
        s.spectro       .wavelength = 250 + 420 # 420 is approximately the middle of the wl range
        s.spectro       .exposure   = 100

        s.spectro.save_path = f"{filename}_signal.asc"
        s.spectro.running   = True
        s.spectro.saved     = True


def take_background(s, filename):
    with temporary(s, "source_shutter", "control", "computer"), \
         temporary(s, "spectro", "shutter", "closed"):
        s.source_shutter.on         = False
        s.spectro       .wavelength = 250 + 420 # 420 is approximately the middle of the wl range
        s.spectro       .exposure   = 100

        s.spectro.save_path = f"{filename}_signal.asc"
        s.spectro.running   = True
        s.spectro.saved     = True


def write_metadata(filename, crystal_mapping, rules):
    with open(filename, "w") as file:
        text = """meta = {

    "crystal_mapping": {
    """
        for pos, value in sorted(crystal_mapping.items()):
            text += f"{repr(pos):>4} : {repr(value):<13},\n"

        text +="}}"
        file.write(text)
