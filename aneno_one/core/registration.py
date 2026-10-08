# SPDX-License-Identifier: GPL-3.0-or-later
"""Register static classes once and coordinate configurable owned UI resources."""
import bpy

from .. import EXTENSION_ID, translations

from .preferences import ANENOONE_Preferences, get_preferences
from .redraw import request_redraw
from .keymap_operators import ANENOONE_OT_keymap_help, ANENOONE_OT_open_keymap_settings
from ..features.language_switch.operators import ANENOONE_OT_language_switch
from ..ui import topbar
from ..ui.sidebar import ANENOONE_PT_language_switch

_CLASSES = (ANENOONE_Preferences, ANENOONE_OT_language_switch,
            ANENOONE_OT_open_keymap_settings, ANENOONE_OT_keymap_help, ANENOONE_PT_language_switch)
_registered = []
_complete = False
_translations_registered = False


def sync_entries(context):
    if not _complete:
        return
    preferences = get_preferences(context)
    topbar.set_enabled(bool(preferences and preferences.enable_language_switch and preferences.show_in_topbar))
    request_redraw(context)


def register():
    global _complete, _translations_registered
    if _complete:
        return
    if _registered or _translations_registered:
        raise RuntimeError("Previous cleanup is incomplete; retry unregister() before enabling")
    try:
        bpy.app.translations.register(EXTENSION_ID, translations.DICTIONARY)
        _translations_registered = True
        for cls in _CLASSES:
            bpy.utils.register_class(cls)
            _registered.append(cls)
        _complete = True
        sync_entries(bpy.context)
    except Exception as error:
        try:
            unregister()
        except Exception as cleanup_error:
            error.add_note(f"Registration rollback failed: {cleanup_error}")
        raise


def unregister():
    global _complete, _translations_registered
    _complete = False
    topbar.set_enabled(False)
    while _registered:
        cls = _registered[-1]
        bpy.utils.unregister_class(cls)
        _registered.pop()
    if _translations_registered:
        bpy.app.translations.unregister(EXTENSION_ID)
        _translations_registered = False
    request_redraw(bpy.context)
