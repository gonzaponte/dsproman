import sys
import time

from itertools import chain

from devserve.clients import SystemClient


class SystemStateManager(SystemClient):
    def __init__(self, *args):
        self._states   = {}
        self._database = {}
        self.logs      = [sys.stdout]

        super().__init__(*args)

    def add_database_entry(self, state_no):
        self._database[state_no] = dict(self._states)

    def log(self, *args, **kwargs):
        for log in self.logs:
            log.write(*args, **kwargs)
            log.flush()

    def save(self, filename):
        self.log(f"{time.asctime()} - Storing database in {filename}")
        columns = sorted(set(chain.from_iterable((d.keys() for d in self._data))))

        lines = [" ".join(["state"] + list(map("_".join, columns)))]
        for state, data in sorted(self._database.items()):
            values = tuple(data.get(column, "nan") for column in columns)
            line   = " ".join((state) + values)
            lines.append(line)

        text = "\n".join(lines + [""])
        open(filename, "w").write(text)

        self.log(f"{time.asctime()} - Database stored successfully")

    def __getattr__(self, device):
        this = self
        sup  = super()
        class Proxy:
            def __getattr__(self, attr):
                if (device, attr) not in this._states:
                    this._states[device, attr] = sup.__getattr__(device).__getattr__(attr)

                return this._states[device, attr]

            def __setattr__(self, attr, value):
                if value == this._states.get((device, attr), None):
                    return

                this.log(f"{time.asctime()} - Setting {device}.{attr} to {value}\n")

                changed = False
                while not changed:
                    sup.__getattr__(device).__setattr__(attr, value)
                    if attr == "shutter":
                        break

                    if attr in "saved running clear_screen".split():
                        # These are not states properties, but rather operations
                        # TODO: change them from properties to methods
                        return

                    from_device = sup.__getattr__(device).__getattr__(attr)
                    if isinstance(from_device, str):
                        from_device = from_device.split("\r")[0].strip()
                    from_device = type(value)(from_device)

                    changed = value == from_device


                this._states[device, attr] = value

                if device == "mono" and attr == "grating":
                    # This forces the wavelength to be updated after
                    # changing grating
                    this._states["mono", "wavelength"] = None

        return Proxy()
