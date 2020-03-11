
def data_taker(s):
    def take_data(filename):
        s.spectro       .save_path = f"{filename}_signal.asc"
        s.power_meter   .save_path = f"{filename}_power.asc"

        s.power_meter.recording = True
        s.spectro    .running   = True
        s.power_meter.recording = False


        s.spectro       .saved     = True
        s.power_meter   .saved     = True
    return take_data
