from . utils import temporary

def take_data(s, filename):
    s.spectro    .save_path = f"{filename}_signal.asc"
    s.power_meter.save_path = f"{filename}_power.asc"

    with temporary(s, "power_meter", "recording", True):
        s.spectro.running   = True

    s.spectro    .saved     = True
    s.power_meter.saved     = True



def write_metadata(filename, crystal_mapping, rules):
    with open(filename, "w") as file:
        file.write("""meta = {

    "crystal_mapping": {
         "0": "SP_B1_003"  ,
         "1": "QZ_B2_080"  ,
         "2": "EmptyHolder",
         "3": "LiF_B2_149" ,
         "4": "ZnO_B3_364" ,
         "5": "Qz_B2_068"  ,
         "6": "empty"      ,
         "7": "empty"      ,
         "8": "empty"      ,
         "9": "empty"      ,
        "10": "empty"      ,
        "11": "empty"      ,
    }
}""")
