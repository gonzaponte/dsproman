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
                sup.__getattr__(device).__setattr__(attr, value)
                if attr in "saved running clear_screen".split():
                    return

                this._states[device, attr] = value

                if device == "mono" and attr == "grating":
                    # This forces the wavelength to be updated after
                    # changing grating
                    this.states["mono", "wavelength"] = None

        return Proxy()
