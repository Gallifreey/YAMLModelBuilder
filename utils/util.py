import ctypes


def get_object_by_id(obj_id: int) -> object:
    """
    Use ctypes to reflect pyobject by its id.
    """
    return ctypes.cast(obj_id, ctypes.py_object).value
