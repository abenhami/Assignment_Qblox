from qcodes import Instrument

from quantify_nano.utilities.general import delete_keys_from_dict

def find_all_subclasses(cls):
    subclasses = cls.__subclasses__()
    return subclasses

def snapshot(update: bool = False, clean: bool = True) -> dict:
    """
    State of all instruments setup as a JSON-compatible dictionary (everything that the
    custom JSON encoder class :class:`qcodes.utils.helpers.NumpyJSONEncoder` supports).

    Parameters
    ----------
    update
        If True, first gets all values before filling the snapshot.
    clean
        If True, removes certain keys from the snapshot to create a more readable and
        compact snapshot.
    """
    snap = {"instruments": {}, "parameters": {}}

    for instrument in find_all_subclasses(Instrument):
        if hasattr(instrument, "instance_list"):
            for instance in instrument.instance_list:
                snap["instruments"][instance.name] = instance.snapshot(update=update)

    if clean:
        exclude_keys = {
            "inter_delay",
            "post_delay",
            "vals",
            "instrument",
            "functions",
            "__class__",
            "raw_value",
            "instrument_name",
            "full_name",
            "val_mapping",
        }
        snap = delete_keys_from_dict(snap, exclude_keys)

    return snap
