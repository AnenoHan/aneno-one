# SPDX-License-Identifier: GPL-3.0-or-later
"""Persist only module and entry-point choices in native AddonPreferences."""
import bpy
from bpy.props import BoolProperty

from .. import EXTENSION_ID
from .metadata import extension_version
from ..features.language_switch.rules import TRANSLATION_CONTEXT


def get_preferences(context):
    preferences = getattr(context, "preferences", None)
    addons = getattr(preferences, "addons", None)
    addon = addons.get(EXTENSION_ID) if addons is not None else None
    return getattr(addon, "preferences", None)


def update_entries(self, context):
    # Import lazily: registration depends on this class definition.
    from . import registration
    registration.sync_entries(context)


class ANENOONE_Preferences(bpy.types.AddonPreferences):
    bl_idname = EXTENSION_ID

    enable_language_switch: BoolProperty(name="Language Switch", description="Enable language switching and its configured entry points",
        translation_context=TRANSLATION_CONTEXT, default=True, update=update_entries)
    show_in_topbar: BoolProperty(name="Show in Topbar", description="Show the language button in the top bar",
        translation_context=TRANSLATION_CONTEXT, default=True, update=update_entries)
    show_in_sidebar: BoolProperty(name="Show in Sidebar", description="Show the language panel in the 3D Viewport sidebar",
        translation_context=TRANSLATION_CONTEXT, default=True, update=update_entries)

    def draw(self, context):
        layout = self.layout
        module = layout.box()
        module.prop(self, "enable_language_switch")
        entries = module.column()
        entries.enabled = self.enable_language_switch
        entries.prop(self, "show_in_topbar")
        entries.prop(self, "show_in_sidebar")
        if not self.enable_language_switch:
            module.label(text="Language Switch is disabled.", text_ctxt=TRANSLATION_CONTEXT)
            module.label(text="Your entry-point settings are retained.", text_ctxt=TRANSLATION_CONTEXT)
        from ..ui.keymap import draw_shortcuts
        draw_shortcuts(module, context, self)
        about = layout.box()
        about.label(text="Aneno One", translate=False)
        version = about.row(align=True)
        version.label(text="Version", text_ctxt=TRANSLATION_CONTEXT)
        version.label(text=extension_version(), translate=False)
        about.label(text="Quality-of-life tools for Blender.", text_ctxt=TRANSLATION_CONTEXT)
