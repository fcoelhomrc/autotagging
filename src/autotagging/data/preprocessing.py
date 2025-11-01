from typing import List


def convert_stringified_list_into_list(s: str) -> List[str]:
    """
    Get list object from inputs in the form 'Item1, Item2, Item3'

    Needed by: colors, material
    """
    split = s.split(",")
    if len(split) < 2:
        return [s.strip()]  # Not a stringified list
    return [s.strip() for s in split]
