#!/usr/bin/env python3
# Copyright 2023 Jon Seager.
# See LICENSE file for licensing details.

"""Polar Signals Cloud Integrator Charm."""

import logging

import ops

logger = logging.getLogger(__name__)


class PolarSignalsCloudIntegratorCharm(ops.CharmBase):
    """Polar Signals Cloud Integrator Charm."""

    def __init__(self, *args):
        super().__init__(*args)

        if not self.unit.is_leader():
            return

        self.framework.observe(self.on.config_changed, self._update)
        self.framework.observe(self.on.parca_store_endpoint_relation_changed, self._update)
        self.framework.observe(self.on.parca_store_endpoint_relation_joined, self._update)

    def _update(self, _):
        """Update relation data with Polar Signals Cloud details."""
        if not (token := self.config["bearer_token"]):
            for relation in self.model.relations["parca-store-endpoint"]:
                relation.data[self.app]["remote-store-bearer-token"] = ""
            self.unit.status = ops.BlockedStatus("no cloud token configured")
        else:
            for relation in self.model.relations["parca-store-endpoint"]:
                relation.data[self.app]["remote-store-address"] = "grpc.polarsignals.com:443"
                relation.data[self.app]["remote-store-bearer-token"] = token
                relation.data[self.app]["remote-store-insecure"] = "false"
            self.unit.status = ops.ActiveStatus()


if __name__ == "__main__":
    ops.main(PolarSignalsCloudIntegratorCharm)
