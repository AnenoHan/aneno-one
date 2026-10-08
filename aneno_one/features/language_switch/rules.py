# SPDX-License-Identifier: GPL-3.0-or-later
"""Pure language decisions; no Blender imports or persistent user state."""
from dataclasses import dataclass

CHINESE = "zh_HANS"
ENGLISH = "en_US"
TARGETS = frozenset((CHINESE, ENGLISH))
TRANSLATION_CONTEXT = "Aneno One"


@dataclass(frozen=True)
class LanguageState:
    raw_locale: str | None
    resolved_locale: str | None
    interface_enabled: bool | None
    translation_flags: tuple[tuple[str, bool], ...]
    available_locales: frozenset[str]
    error: str | None = None


@dataclass(frozen=True)
class LanguageAction:
    kind: str
    target: str | None = None
    reason: str | None = None


@dataclass(frozen=True)
class ApplyResult:
    ok: bool
    changed: bool = False
    error: str | None = None
    rollback_error: str | None = None
    detail: str | None = None


@dataclass(frozen=True)
class LanguageDisplay:
    label: str
    tooltip: str


def is_english(locale):
    return locale == "en" or locale.startswith("en_")


def resolve_action(state, target="AUTO"):
    if target not in TARGETS and target != "AUTO":
        return LanguageAction("UNAVAILABLE", reason="INVALID_TARGET")
    if (state.error is not None or not state.raw_locale or state.interface_enabled is None
            or state.raw_locale not in state.available_locales):
        return LanguageAction("UNAVAILABLE", reason="STATE_UNAVAILABLE")
    if target == "AUTO":
        if state.raw_locale == CHINESE:
            target = ENGLISH
        elif is_english(state.raw_locale):
            target = CHINESE
        else:
            return LanguageAction("CHOOSE")
    if target not in state.available_locales:
        return LanguageAction("UNAVAILABLE", reason="TARGET_UNAVAILABLE")
    return LanguageAction("APPLY", target)


def language_display(state, translate=lambda message: message):
    locale = state.raw_locale
    if (state.error is not None or not locale or state.interface_enabled is None
            or locale not in state.available_locales):
        return LanguageDisplay("?", translate("Language settings are unavailable. No settings will be changed."))
    if locale == CHINESE:
        if state.interface_enabled:
            return LanguageDisplay("中", translate("Current language setting: Simplified Chinese. Click to switch to English."))
        return LanguageDisplay("中*", translate("Current language setting: Simplified Chinese; interface translation is off. Click to switch to English."))
    if is_english(locale):
        return LanguageDisplay("EN", translate("Current language setting: English. Click to switch to Simplified Chinese."))
    if locale == "DEFAULT":
        return LanguageDisplay("AUTO", translate("Current language setting: Automatic. Click to choose Simplified Chinese or English."))
    label = {"zh_HANT": "ZH-T", "ja_JP": "JA", "fr_FR": "FR", "de_DE": "DE"}.get(locale, locale)
    return LanguageDisplay(label, translate("Current language setting: {locale}. Click to choose Simplified Chinese or English.").format(locale=locale))
