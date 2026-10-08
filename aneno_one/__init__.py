# SPDX-License-Identifier: GPL-3.0-or-later
"""Aneno One extension entry point."""

EXTENSION_ID = __package__

from .core import registration


def register():
    registration.register()


def unregister():
    registration.unregister()
