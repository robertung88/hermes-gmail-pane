"""Agent half of the Gmail desktop plugin package.

The feature is entirely a desktop surface (page, pane, and its own backend), so
this half registers nothing: no tools, hooks, slash commands or env vars. It
exists so the package is importable, and because ``plugins.enabled`` is the gate
that lets the gateway import ``dashboard/plugin_api.py``.
"""

from __future__ import annotations


def register(ctx) -> None:  # noqa: ARG001
    """The Gmail UI and API are owned by the Desktop/dashboard surfaces."""
    return None
