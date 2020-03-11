from devserve.clients import SystemClient


class SystemStateManager(SystemClient):
    def __init__(self, *args, extra_logs=()):
        self._states = {}

        self.logs = [sys.stdout, *extra_logs]

        super().__init__(*args)

    def log(self, *args, **kwargs):
        for log in self.logs:
            log.write(*args, **kwargs)
            log.flush()

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
                    changed = value == sup.__getattr__(device).__getattr__(attr)

                if attr in "saved recording running clear_screen".split():
                    # These are not states properties, but rather operations
                    # TODO: change them from properties to methods
                    return

                this._states[device, attr] = value

                if device == "mono" and attr == "grating":
                    # This forces the wavelength to be updated after
                    # changing grating
                    this.states["mono", "wavelength"] = None

        return Proxy()
