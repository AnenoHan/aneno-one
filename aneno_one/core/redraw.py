# SPDX-License-Identifier: GPL-3.0-or-later
"""One-shot redraw requests; no subscriptions, handlers or polling."""


def request_redraw(context):
    manager = getattr(context, "window_manager", None)
    if manager is None:
        return
    for window in manager.windows:
        try:
            for area in window.screen.areas:
                if area.type in {'TOPBAR', 'VIEW_3D', 'PREFERENCES'}:
                    area.tag_redraw()
        except ReferenceError:
            # A window can be closed while its areas are being invalidated.
            continue
