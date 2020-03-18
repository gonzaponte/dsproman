import contextlib

@contextlib.contextmanager
def temporary(device, attribute, temp_value):
    old_value = getattr(getattr(s, device), attribute)
    try:
        setattr(getattr(s, device), attribute, temp_value)
        yield None
    finally:
        setattr(getattr(s, device), attribute, old_value)
