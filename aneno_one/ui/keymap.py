# SPDX-License-Identifier: GPL-3.0-or-later
"""Presentation of read-only shortcut snapshots and native setup guidance."""
import bpy

from ..features.language_switch.rules import TRANSLATION_CONTEXT
from ..translations import iface
from ..core.keymap import access_status, query_shortcut_bindings, shortcut_status

STATUS_LABELS = {'ASSIGNED': 'Assigned', 'NOT_ASSIGNED': 'Not Assigned',
                 'DISABLED': 'Disabled', 'UNKNOWN': 'Unknown'}
REASON_LABELS = {'DISABLED': 'Disabled', 'MODAL': 'Modal binding', 'EMPTY_EVENT': 'No input event',
                 'INVALID_EVENT': 'Invalid input event', 'NOT_DIRECT_INPUT': 'Not a direct input event'}
HELP_LINES = (
    '1. Open Keymap Settings and clear the search field.',
    '2. Expand Window and scroll to its Add New button.',
    '3. Click Add New, then expand the new item.',
    '4. Enter this Operator ID:',
    '5. Choose a key and any modifiers; keep the item enabled.',
    '6. Return to the main window to try your shortcut.',
    'Window applies across editors; other keymaps have a limited scope.',
    'Other shortcuts or modal tools may intercept the same input.',
    'If automatic saving is off, use Save Preferences to keep changes.',
    'Searching by name may be empty until a binding exists.',
)


def draw_keymap_help(layout):
    for index, line in enumerate(HELP_LINES):
        layout.label(text=line, text_ctxt=TRANSLATION_CONTEXT)
        if index == 3:
            layout.label(text='aneno_one.language_switch', translate=False)


def draw_shortcuts(layout, context, preferences):
    snapshot = query_shortcut_bindings(context)
    box = layout.box()
    title = box.row(align=True)
    title.label(text='Shortcut', text_ctxt=TRANSLATION_CONTEXT)
    title.label(text=STATUS_LABELS[shortcut_status(snapshot)], text_ctxt=TRANSLATION_CONTEXT)
    if not snapshot.available:
        box.label(text='Unable to read shortcut settings.', text_ctxt=TRANSLATION_CONTEXT)
    for binding in snapshot.bindings:
        item = box.box()
        row = item.row(align=True)
        row.label(text=binding.display or binding.event_type, translate=False)
        row.label(text='Enabled' if binding.effective else REASON_LABELS[binding.ineffective_reason], text_ctxt=TRANSLATION_CONTEXT)
        scope = item.row(align=True)
        scope.label(text='Keymap', text_ctxt=TRANSLATION_CONTEXT)
        scope.label(text=binding.keymap_name, translate=False)
        # Preserve user-defined keymap names; editor/region labels come from native RNA.
        scope = item.row(align=True)
        scope.label(text='Editor / Region', text_ctxt=TRANSLATION_CONTEXT)
        scope.label(text=scope_label(binding), translate=False)
    if snapshot.bindings:
        box.label(text='Bindings apply in their listed keymap context.', text_ctxt=TRANSLATION_CONTEXT)
    access = access_status(preferences.enable_language_switch, preferences.show_in_topbar,
                           preferences.show_in_sidebar, snapshot)
    if access == 'NO_ENTRY':
        warning = box.column()
        warning.alert = True
        warning.label(text='No direct access to Language Switch.', text_ctxt=TRANSLATION_CONTEXT)
        warning.label(text='Enable an entry point or assign a shortcut.', text_ctxt=TRANSLATION_CONTEXT)
    elif access == 'UNKNOWN':
        box.label(text='Both entry points are hidden; shortcut access is unknown.', text_ctxt=TRANSLATION_CONTEXT)
    row = box.row(align=True)
    row.operator_context = 'INVOKE_DEFAULT'
    row.operator('aneno_one.open_keymap_settings')
    row.operator('aneno_one.keymap_help', text='How to Add a Shortcut', text_ctxt=TRANSLATION_CONTEXT)
    box.label(text='No shortcut is assigned automatically.', text_ctxt=TRANSLATION_CONTEXT)


def scope_label(binding):
    def label(property_name, identifier):
        prop = bpy.types.KeyMap.bl_rna.properties[property_name]
        item = prop.enum_items.get(identifier)
        return (bpy.app.translations.pgettext_iface(item.name, prop.translation_context)
                if item else identifier)
    editor = (iface('Any Editor') if binding.space_type == 'EMPTY'
              else label('space_type', binding.space_type))
    return f"{editor} / {label('region_type', binding.region_type)}"
