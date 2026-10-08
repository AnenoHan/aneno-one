# SPDX-License-Identifier: GPL-3.0-or-later
"""Delegate locale resolution and category switches to Blender."""
import bpy

from ..features.language_switch.rules import TRANSLATION_CONTEXT
from .zh_hans import MESSAGES

DICTIONARY = {'zh_HANS': {(TRANSLATION_CONTEXT, source): target
                          for source, target in MESSAGES.items()}}
# RNA property labels use translation_context, but native property tooltips
# look up their descriptions in the default context in Blender 5.x.
# Alias only our three complete, specific descriptions, never generic labels.
PROPERTY_DESCRIPTIONS = (
    'Enable language switching and its configured entry points',
    'Show the language button in the top bar',
    'Show the language panel in the 3D Viewport sidebar',
)
DICTIONARY['zh_HANS'].update({('*', message): MESSAGES[message]
                            for message in PROPERTY_DESCRIPTIONS})
# Windows Automatic locale uses script title case; explicit Blender selection
# uses zh_HANS. Register both native spellings against the same message catalog.
DICTIONARY['zh_Hans'] = DICTIONARY['zh_HANS']


def iface(message):
    return bpy.app.translations.pgettext_iface(message, TRANSLATION_CONTEXT)


def tip(message):
    return bpy.app.translations.pgettext_tip(message, TRANSLATION_CONTEXT)


def rpt(message):
    return bpy.app.translations.pgettext_rpt(message, TRANSLATION_CONTEXT)
