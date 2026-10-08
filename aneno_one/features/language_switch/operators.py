# SPDX-License-Identifier: GPL-3.0-or-later
"""Stable operator shared by Topbar, future Sidebar and user key bindings."""
import bpy
from bpy.props import StringProperty

from ...core.preferences import get_preferences
from ...core.redraw import request_redraw
from ...translations import iface, tip, rpt
from .rules import CHINESE, ENGLISH, TRANSLATION_CONTEXT, language_display, resolve_action
from .service import apply_language, read_language_state


def module_enabled(context):
    preferences = get_preferences(context)
    return bool(preferences and preferences.enable_language_switch)


def draw_language_choices(menu, context):
    state = read_language_state(context)
    menu.layout.operator_context = 'EXEC_DEFAULT'
    for target, label in ((CHINESE, "Simplified Chinese"), (ENGLISH, "English")):
        row = menu.layout.row()
        row.enabled = module_enabled(context) and target in state.available_locales
        row.operator(ANENOONE_OT_language_switch.bl_idname, text=label,
                     text_ctxt=TRANSLATION_CONTEXT).target = target


class ANENOONE_OT_language_switch(bpy.types.Operator):
    bl_idname = "aneno_one.language_switch"
    bl_label = "Switch Language"
    bl_description = "Switch between Simplified Chinese and English"
    bl_translation_context = TRANSLATION_CONTEXT
    bl_options = set()

    target: StringProperty(default="AUTO", options={'HIDDEN', 'SKIP_SAVE'})

    @classmethod
    def poll(cls, context):
        enabled = module_enabled(context)
        if not enabled:
            cls.poll_message_set(tip("Language Switch is disabled"))
        return enabled

    @classmethod
    def description(cls, context, properties):
        target = properties.target
        if target == CHINESE:
            message = "Set the language to Simplified Chinese and enable interface translation."
        elif target == ENGLISH:
            message = "Set the language to English."
        else:
            return language_display(read_language_state(context), translate=tip).tooltip
        return tip(message)

    def invoke(self, context, event):
        if not module_enabled(context):
            self.report({'WARNING'}, rpt("Language Switch is disabled"))
            return {'CANCELLED'}
        action = resolve_action(read_language_state(context), self.target)
        if action.kind == "CHOOSE":
            if bpy.app.background or getattr(context, "window", None) is None:
                self.report({'WARNING'}, rpt("Choose an explicit language target; no interactive window is available"))
                return {'CANCELLED'}
            context.window_manager.popup_menu(draw_language_choices, title=iface("Choose Language"))
            return {'FINISHED'}
        return self.execute(context)

    def execute(self, context):
        if not module_enabled(context):
            self.report({'WARNING'}, rpt("Language Switch is disabled"))
            return {'CANCELLED'}
        action = resolve_action(read_language_state(context), self.target)
        if action.kind != "APPLY":
            messages = {
                "INVALID_TARGET": "Invalid language target",
                "STATE_UNAVAILABLE": "Language settings are unavailable; no settings were changed",
                "TARGET_UNAVAILABLE": "The requested language is unavailable in this Blender installation",
            }
            message = ("Choose Simplified Chinese or English explicitly" if action.kind == "CHOOSE"
                       else messages.get(action.reason, "Language switch is unavailable"))
            self.report({'WARNING'}, rpt(message))
            return {'CANCELLED'}
        result = apply_language(context, action.target)
        request_redraw(context)
        if not result.ok:
            message = rpt("Language switch failed ({error}): {detail}").format(
                error=result.error, detail=result.detail or "")
            if result.rollback_error is not None:
                message += rpt(". Settings could not be fully restored: {detail}").format(
                    detail=result.rollback_error)
            self.report({'WARNING'}, message)
            return {'CANCELLED'}
        return {'FINISHED'}
