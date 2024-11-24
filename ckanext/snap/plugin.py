"""Definition of the main plugin.
"""

from __future__ import annotations
from typing import Any

from ckan import types
import ckan.plugins as p
import ckan.plugins.toolkit as tk
from . import subscriptions


@tk.blanket.actions
@tk.blanket.blueprints
@tk.blanket.auth_functions
@tk.blanket.config_declarations
class SnapPlugin(
    p.SingletonPlugin,
):
    p.implements(p.ISignal)
    p.implements(p.IConfigurer, inherit=True)

    def get_signal_subscriptions(self) -> types.SignalMapping:
        return {
            tk.signals.action_succeeded: [subscriptions.make_snapshot_listener],
        }


    def update_config(self, config_: Any):
        tk.add_template_directory(config_, "templates")
        tk.add_resource("assets", "files")
