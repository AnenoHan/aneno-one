# SPDX-License-Identifier: GPL-3.0-or-later
"""Own exactly one header callback, drawing in the right region only."""
import bpy

from ..core.preferences import get_preferences
from .language import draw_language_button

_attached = False


def draw_language_switch(self, context):
    if getattr(getattr(context, "region", None), "alignment", None) != 'RIGHT':
        return
    preferences = get_preferences(context)
    if not preferences or not preferences.enable_language_switch or not preferences.show_in_topbar:
        return
    draw_language_button(self.layout, context)


def set_enabled(enabled):
    global _attached
    if enabled and not _attached:
        bpy.types.TOPBAR_HT_upper_bar.append(draw_language_switch)
        _attached = True
    elif not enabled and _attached:
        bpy.types.TOPBAR_HT_upper_bar.remove(draw_language_switch)
        _attached = False
