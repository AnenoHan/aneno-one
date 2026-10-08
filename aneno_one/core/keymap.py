# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only snapshots of Blender's final user key configuration."""
from dataclasses import dataclass

OPERATOR_ID = "aneno_one.language_switch"
INPUT_MAP_TYPES = frozenset({'KEYBOARD', 'MOUSE', 'NDOF', 'TEXTINPUT'})


@dataclass(frozen=True)
class ShortcutBinding:
    keymap_name: str
    space_type: str
    region_type: str
    display: str
    event_type: str
    event_value: str
    active: bool
    is_modal: bool
    effective: bool
    ineffective_reason: str | None


@dataclass(frozen=True)
class ShortcutSnapshot:
    available: bool
    bindings: tuple[ShortcutBinding, ...] = ()
    error: str | None = None


def binding_reason(active, is_modal, event_type, event_value, map_type, types, values):
    if not active:
        return 'DISABLED'
    if is_modal:
        return 'MODAL'
    if event_type == 'NONE':
        return 'EMPTY_EVENT'
    if event_type not in types or event_value not in values:
        return 'INVALID_EVENT'
    if map_type not in INPUT_MAP_TYPES:
        return 'NOT_DIRECT_INPUT'
    return None


def query_shortcut_bindings(context):
    try:
        config = context.window_manager.keyconfigs.user
        if config is None:
            return ShortcutSnapshot(False, error='USER_KEYCONFIG_UNAVAILABLE')
        bindings = []
        for keymap in config.keymaps:
            for item in keymap.keymap_items:
                if item.idname != OPERATOR_ID:
                    continue
                event_type, event_value = item.type, item.value
                properties = item.bl_rna.properties
                types = {entry.identifier for entry in properties['type'].enum_items}
                values = {entry.identifier for entry in properties['value'].enum_items}
                reason = binding_reason(item.active, keymap.is_modal, event_type, event_value,
                                        item.map_type, types, values)
                display = item.to_string()
                if not isinstance(display, str):
                    raise ValueError('Key binding could not be formatted')
                bindings.append(ShortcutBinding(keymap.name, keymap.space_type, keymap.region_type,
                                                display, event_type, event_value, item.active,
                                                keymap.is_modal, reason is None, reason))
        return ShortcutSnapshot(True, tuple(bindings))
    except Exception as error:
        # A partial scan must never claim there are no working bindings.
        return ShortcutSnapshot(False, error=str(error) or type(error).__name__)


def shortcut_status(snapshot):
    if not snapshot.available:
        return 'UNKNOWN'
    if any(binding.effective for binding in snapshot.bindings):
        return 'ASSIGNED'
    if snapshot.bindings and all(not binding.active for binding in snapshot.bindings):
        return 'DISABLED'
    return 'NOT_ASSIGNED'


def access_status(module_enabled, topbar_visible, sidebar_visible, snapshot):
    if not module_enabled:
        return 'MODULE_DISABLED'
    if topbar_visible or sidebar_visible:
        return 'AVAILABLE'
    status = shortcut_status(snapshot)
    if status == 'UNKNOWN':
        return 'UNKNOWN'
    return 'AVAILABLE' if status == 'ASSIGNED' else 'NO_ENTRY'
