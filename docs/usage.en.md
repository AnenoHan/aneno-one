# Aneno One 0.1.0 User Guide

[简体中文](usage.zh-CN.md) · [Project overview](../README.md) · [Version notes](../CHANGELOG.md)

## 1. Features and compatibility

Aneno One provides quick switching between English and Simplified Chinese. Use the right-hand Topbar button, the 3D Viewport sidebar, or a shortcut you assign. In the add-on preferences, you can toggle either UI entry, inspect the actual shortcut state and check the version under About.

This version was verified on Windows 11 with Blender 5.2.2 LTS. The manifest minimum is 5.0.0. Blender 5.0.0 and 5.1.2 have historical development-build test results, but version 0.1.0 has not been retested on them. English-language Windows, Linux, macOS and additional display configurations remain unverified.

## 2. Install or upgrade

1. Obtain the **aneno_one-0.1.0.zip** extension package. Do not extract it.
2. Open **Edit → Preferences → Get Extensions**. Choose **Install from Disk** from the top-right menu, select the ZIP and complete installation.
3. Under **Add-ons**, make sure Aneno One is enabled. Expand its preferences and confirm that About shows **0.1.0**.
4. On a fresh installation, Language Switch, Topbar and Sidebar are enabled. Press **N** in the 3D Viewport and select the **Aneno One** tab.
5. To upgrade an older or candidate version, use the same local extension repository and upgrade in place. Avoid duplicate installations. You do not need to uninstall first or recreate shortcuts; existing language, entry choices and manual bindings should remain intact.

Use the extension package for installation. Do not copy the source archive directly into the legacy `scripts/addons` directory.

## 3. Switch languages

| Button | Meaning | Action when clicked |
|---|---|---|
| EN | The language setting is English | Switch to Simplified Chinese and enable native Interface Translation |
| 中 | Simplified Chinese with interface translation enabled | Switch to English |
| 中* | Simplified Chinese with interface translation disabled | Switch to English |
| AUTO | Automatic language selection | Open the English/Chinese choice; Escape cancels |
| Other abbreviation | Another language is selected | Open the English/Chinese choice; Escape cancels |

The button reflects Blender's language setting. It does not guarantee that every visible string has a translation. AUTO may differ from the language currently used by the interface.

Switching to Chinese enables native Interface Translation. Other translation flags, including tooltips, reports and new data, retain their existing values. Switching to English also preserves those flags. A language change can still affect translated tooltips or names of subsequently created data. The extension does not rename existing objects or other data.

## 4. Module and entry controls

Under **Preferences → Add-ons → Aneno One**, you can disable Topbar or Sidebar independently. Disabling the Language Switch module hides its entries and prevents switching. Re-enabling it restores your previous entry choices.

You can hide both entries and use a manual shortcut. If no usable binding exists either, the add-on prompts you to enable an entry or assign a shortcut; it does not change your configuration automatically.

## 5. Assign a shortcut

No shortcut is created by default. The shortcut display reads Blender's current bindings without adding, replacing or deleting them.

1. Click **Open Keymap Settings** in the add-on preferences and clear the native Keymap search field.
2. Expand **Window**, scroll to its **Add New** button, click it and expand the new item.
3. Set the Operator ID to `aneno_one.language_switch`.
4. Choose a key and any modifiers, keeping the item enabled. Avoid conflicts with existing shortcuts.
5. Return to the main window and test switching in both directions. Searching by the add-on name may return nothing until a binding exists.
6. If Auto-Save Preferences is off, save preferences manually to retain the binding.

Window bindings apply across editors. Bindings in other keymaps are limited to their contexts. Other shortcuts or modal tools may intercept the same input; Aneno One does not resolve conflicts automatically. Multiple bindings, disabled states and their scope are shown in the add-on preferences.

To remove a binding, delete its item in Blender's native Keymap settings. The add-on display follows the actual state.

## 6. Save settings

Language, entry choices and key bindings follow Blender's native preference-saving behavior. With Auto-Save Preferences enabled, Blender saves the changes. With it disabled, choose **Save Preferences** from the preferences menu.

Saving a `.blend` file does not save preferences. Aneno One does not force a global preference save or maintain a separate copy of the language or keymap state.

## 7. Disable or uninstall

Disable Aneno One from the Add-ons page, or uninstall it through the native extension menu. The extension removes its own registered UI and resources while preserving the current language and user-created key bindings.

A binding cannot execute the extension after it has been uninstalled. Remove unwanted bindings manually in Keymap settings.

## 8. Known limitations and troubleshooting

1. The native Topbar can become blank after window or layout changes. Manually maximizing and restoring the window can usually recover it. This has been observed with and without the extension and remains unfixed.
2. Historical Blender 5.1 testing also recorded a two-window crash and a Win32 1407 failure when a script created a window after saving. Unrestricted multi-window reliability on that version is not established.
3. An already-open tooltip may retain its old language. Move the pointer away and hover again to recreate it.
4. A maximized or full-screen editor without a Topbar cannot display the Topbar button. Use the Sidebar or a manual shortcut where available.
5. If a button is missing, check the module and entry switches. If a shortcut does not work, check its enabled state, context and possible conflicts.

When reporting an issue, include the add-on version, Blender version, operating system, reproduction steps, and expected and actual behavior. Remove personal information, file paths and unrelated project content from screenshots and logs before sharing them.

## 9. License

Aneno One is licensed under [GPL-3.0-or-later](../LICENSE). It has no third-party runtime dependencies, requests no additional permissions and includes no telemetry, network service or built-in updater. Maintainer: **Aneno**.
