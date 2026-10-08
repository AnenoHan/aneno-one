# SPDX-License-Identifier: GPL-3.0-or-later
"""Render the same current-state action in each language entry point."""
from ..features.language_switch.rules import language_display
from ..features.language_switch.service import read_language_state


def draw_language_button(layout, context):
    display = language_display(read_language_state(context))
    row = layout.row(align=True)
    row.operator_context = 'INVOKE_DEFAULT'
    row.operator("aneno_one.language_switch", text=display.label, translate=False).target = "AUTO"
