# SPDX-License-Identifier: GPL-3.0-or-later
"""Read release metadata from the installed manifest, without writing files."""
from functools import lru_cache
from pathlib import Path
import tomllib


@lru_cache(maxsize=1)
def extension_version():
    manifest = Path(__file__).resolve().parents[1] / "blender_manifest.toml"
    with manifest.open("rb") as stream:
        return tomllib.load(stream)["version"]
