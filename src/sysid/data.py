"""
sysid.data
==========

Loaders for the original SYSID course datasets stored in this repository.

Each loader returns plain 1-D NumPy arrays ``(y, u, time)`` so notebooks stay
clean. CSV files are read with NumPy (no pandas); MATLAB ``.mat`` files are
read with SciPy.

Usage
-----
    from sysid import readData

    y, u, time = readData("quarter_drone")                 # default dataset
    y, u, time = readData("ball_and_hoop", "closedLoop")
    y, u, time, yref = readData("quarter_drone", return_ref=True)

Only datasets hosted in this repo are exposed here. Externally hosted case
studies (ball-and-beam, wind blade, IFAC2015 LPV) keep loading from their
own sources in the respective notebooks.
"""

import os
import tempfile
import urllib.request

import numpy as np
import scipy.io

# Raw base URL for data files committed to this repository.
_RAW_BASE = "https://raw.githubusercontent.com/helonayala/sysid/main/data"

# Local cache directory used when the file is not already available on disk.
_CACHE_DIR = os.path.join(tempfile.gettempdir(), "sysid_data")

# Registry of our original datasets: (case_study, dataset) -> spec.
# For CSV files, ``cols`` maps the returned vectors to column indices.
_REGISTRY = {
    ("quarter_drone", "dados"): {
        "path": "quarter_drone/dados_14_drone.csv",
        "kind": "csv",
        "cols": {"time": 0, "y": 1, "u": 2, "ref": 3},
    },
    ("quarter_drone", "seq"): {
        "path": "quarter_drone/14_drone_seq_20260529_195254.csv",
        "kind": "csv",
        "cols": {"time": 0, "y": 1, "u": 2, "ref": 3},
    },
    ("ball_and_hoop", "closedLoop"): {
        "path": "ball_and_hoop/closedLoop.mat",
        "kind": "mat",
    },
    ("ball_and_hoop", "fixedStepSequence"): {
        "path": "ball_and_hoop/fixedStepSequence.mat",
        "kind": "mat",
    },
    ("ball_and_hoop", "randomStepSequence"): {
        "path": "ball_and_hoop/randomStepSequence.mat",
        "kind": "mat",
    },
}

# Default dataset per case study (used when ``dataset`` is omitted).
_DEFAULT_DATASET = {
    "quarter_drone": "dados",
    "ball_and_hoop": "closedLoop",
}


def _resolve(relpath):
    """Return a local path to ``relpath``.

    Prefers a copy already on disk under ``data/`` (e.g. when running inside a
    checkout of this repository, such as the Jupyter Book build). Otherwise
    downloads it from the repository's raw URL into a local cache.
    """
    local = os.path.join("data", relpath)
    if os.path.exists(local):
        return local

    os.makedirs(_CACHE_DIR, exist_ok=True)
    dest = os.path.join(_CACHE_DIR, relpath.replace("/", "_"))
    if not os.path.exists(dest):
        url = f"{_RAW_BASE}/{relpath}"
        urllib.request.urlretrieve(url, dest)
    return dest


def list_datasets():
    """Return the available ``(case_study, dataset)`` keys."""
    return sorted(_REGISTRY.keys())


def readData(case_study, dataset=None, *, return_ref=False):
    """Load an original SYSID dataset as ``(y, u, time)`` NumPy vectors.

    Args:
        case_study (str): e.g. ``"quarter_drone"`` or ``"ball_and_hoop"``.
        dataset (str, optional): Which dataset within the case study. If
            omitted, a sensible default is used.
        return_ref (bool): If True, also return the reference signal
            (``referencia`` for CSVs, ``yref`` for ``.mat`` files) as a 4th
            value; an empty array is returned when no reference exists.

    Returns:
        (y, u, time) or (y, u, time, ref): 1-D float NumPy arrays.
    """
    if dataset is None:
        dataset = _DEFAULT_DATASET.get(case_study)
        if dataset is None:
            raise ValueError(
                f"Unknown case study {case_study!r}. "
                f"Available: {sorted(_DEFAULT_DATASET)}"
            )

    spec = _REGISTRY.get((case_study, dataset))
    if spec is None:
        raise ValueError(
            f"Unknown dataset ({case_study!r}, {dataset!r}). "
            f"Available: {list_datasets()}"
        )

    fpath = _resolve(spec["path"])

    if spec["kind"] == "csv":
        arr = np.genfromtxt(fpath, delimiter=",", skip_header=1)
        c = spec["cols"]
        time = arr[:, c["time"]]
        y = arr[:, c["y"]]
        u = arr[:, c["u"]]
        ref = arr[:, c["ref"]] if "ref" in c else np.array([])
    elif spec["kind"] == "mat":
        mat = scipy.io.loadmat(fpath)
        time = np.asarray(mat["time"], dtype=float).reshape(-1)
        u = np.asarray(mat["u"], dtype=float).reshape(-1)
        y = np.asarray(mat["y"], dtype=float).reshape(-1)
        yref = mat.get("yref")
        if yref is not None and getattr(yref, "size", 0) > 0:
            ref = np.asarray(yref, dtype=float).reshape(-1)
        else:
            ref = np.array([])
    else:  # pragma: no cover - guarded by registry
        raise ValueError(f"Unsupported dataset kind: {spec['kind']!r}")

    if return_ref:
        return y, u, time, ref
    return y, u, time
