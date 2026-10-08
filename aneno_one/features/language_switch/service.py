# SPDX-License-Identifier: GPL-3.0-or-later
"""Read Blender state and apply only the two permitted preference changes."""
import bpy

from .rules import ApplyResult, CHINESE, LanguageState, TARGETS, resolve_action


def read_language_state(context):
    try:
        view = context.preferences.view
        flags = tuple((prop.identifier, bool(getattr(view, prop.identifier)))
                      for prop in view.bl_rna.properties
                      if prop.identifier.startswith("use_translate_"))
        locales = frozenset(item.identifier for item in view.bl_rna.properties["language"].enum_items
                            if item.identifier)
        return LanguageState(view.language, bpy.app.translations.locale,
                             view.use_translate_interface, flags, locales)
    except Exception as error:
        return LanguageState(None, None, None, (), frozenset(), str(error))


def _apply_to_view(view, state, target):
    """Transaction boundary, also exercised with failing RNA-like adapters."""
    if target not in TARGETS:
        return ApplyResult(False, error="INVALID_TARGET")
    action = resolve_action(state, target)
    if action.kind != "APPLY":
        return ApplyResult(False, error=action.reason, detail=state.error)
    planned = [("language", state.raw_locale, target)]
    if target == CHINESE:
        planned.append(("use_translate_interface", state.interface_enabled, True))
    attempted = []
    try:
        for field, before, after in planned:
            if before != after:
                # Keep ownership even if a setter mutates and then raises.
                attempted.append((field, before))
                setattr(view, field, after)
                if getattr(view, field) != after:
                    raise RuntimeError(f"{field} did not retain its requested value")
    except Exception as error:
        failures = []
        for field, before in reversed(attempted):
            try:
                setattr(view, field, before)
                if getattr(view, field) != before:
                    raise RuntimeError("Restored value could not be verified")
            except Exception as rollback_error:
                failures.append(f"{field}: {rollback_error}")
        return ApplyResult(False, error="WRITE_FAILED", detail=str(error),
                           rollback_error="; ".join(failures) or None)
    return ApplyResult(True, changed=bool(attempted))


def apply_language(context, target):
    state = read_language_state(context)
    if state.error is not None:
        return ApplyResult(False, error="STATE_UNAVAILABLE", detail=state.error)
    return _apply_to_view(context.preferences.view, state, target)
