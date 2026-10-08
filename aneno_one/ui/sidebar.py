# SPDX-License-Identifier: GPL-3.0-or-later
"""Native 3D View entry; visibility follows the existing preference choices."""
import bpy

from ..core.preferences import get_preferences
from ..features.language_switch.rules import TRANSLATION_CONTEXT
from .language import draw_language_button


class ANENOONE_PT_language_switch(bpy.types.Panel):
    bl_idname = "ANENOONE_PT_language_switch"
    bl_label = "Language Switch"
    bl_translation_context = TRANSLATION_CONTEXT
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Aneno One"

    @classmethod
    def poll(cls, context):
        preferences = get_preferences(context)
        return bool(preferences and preferences.enable_language_switch and preferences.show_in_sidebar)

    def draw(self, context):
        draw_language_button(self.layout, context)
