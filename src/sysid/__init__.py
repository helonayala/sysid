"""
sysid
=====

System identification course library: data-driven model methods (NARX with
FROLS term selection) plus loaders for the original course datasets.

    pip install git+https://github.com/helonayala/sysid.git

    import sysid as si
    from sysid import NARX, readData
"""

from .narx import NARX, regMatARX, regMatNARX, frols_py
from .data import readData, list_datasets

__version__ = "0.1.0"

__all__ = [
    "NARX",
    "regMatARX",
    "regMatNARX",
    "frols_py",
    "readData",
    "list_datasets",
]
