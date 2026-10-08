# SPDX-License-Identifier: GPL-3.0-or-later
"""Open native settings and explain manual binding without editing keymaps."""
import bpy

from ..features.language_switch.rules import TRANSLATION_CONTEXT
from ..ui.keymap import draw_keymap_help
from ..translations import rpt, tip


def has_window(context):
    return not bpy.app.background and getattr(context, 'window', None) is not None


class ANENOONE_OT_open_keymap_settings(bpy.types.Operator):
    bl_idname = 'aneno_one.open_keymap_settings'
    bl_label = 'Open Keymap Settings'
    bl_description = 'Open Blender keymap preferences without creating a shortcut'
    bl_translation_context = TRANSLATION_CONTEXT
    bl_options = set()

    @classmethod
    def description(cls, context, properties):
        return tip(cls.bl_description)

    @classmethod
    def poll(cls, context):
        return has_window(context)

    def execute(self, context):
        if not has_window(context):
            self.report({'WARNING'}, rpt('An interactive window is required to open Keymap Settings'))
            return {'CANCELLED'}
        try:
            if getattr(getattr(context, 'area', None), 'type', None) != 'PREFERENCES':
                result = bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
                if 'FINISHED' not in result:
                    self.report({'WARNING'}, rpt('Blender could not open Preferences'))
                    return {'CANCELLED'}
            context.preferences.active_section = 'KEYMAP'
            for window in context.window_manager.windows:
                for area in window.screen.areas:
                    if area.type == 'PREFERENCES':
                        area.spaces.active.filter_text = ''
                        area.tag_redraw()
        except (RuntimeError, AttributeError, ReferenceError) as error:
            self.report({'WARNING'}, rpt('Unable to open Keymap Settings: {detail}').format(detail=error))
            return {'CANCELLED'}
        return {'FINISHED'}


class ANENOONE_OT_keymap_help(bpy.types.Operator):
    bl_idname = 'aneno_one.keymap_help'
    bl_label = 'How to Add a Shortcut'
    bl_description = 'Show the steps to add a shortcut using Blender preferences'
    bl_translation_context = TRANSLATION_CONTEXT
    bl_options = set()

    @classmethod
    def description(cls, context, properties):
        return tip(cls.bl_description)

    @classmethod
    def poll(cls, context):
        return has_window(context)

    def draw(self, context):
        draw_keymap_help(self.layout)

    def invoke(self, context, event):
        if not has_window(context):
            return {'CANCELLED'}
        return context.window_manager.invoke_popup(self, width=560)

    def execute(self, context):
        if not has_window(context):
            return {'CANCELLED'}
        return {'FINISHED'}
