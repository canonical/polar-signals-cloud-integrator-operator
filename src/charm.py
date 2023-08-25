#!/usr/bin/env python3
# Copyright 2023 Jon Seager.
# See LICENSE file for licensing details.

"""Polar Signals Cloud Integrator Charm."""

import logging

import ops
from charms.parca.v0.parca_store import ParcaStoreEndpointProvider

logger = logging.getLogger(__name__)


class PolarSignalsCloudIntegratorCharm(ops.CharmBase):
    """Polar Signals Cloud Integrator Charm."""

    def __init__(self, *args):
        super().__init__(*args)

        if not self.unit.is_leader():
            return

        self.framework.observe(self.on.config_changed, self._update)
        self.framework.observe(self.on.update_status, self._update)

        self.store_provider = ParcaStoreEndpointProvider(
            self,
            port=443,
            insecure=False,
            external_url="https://grpc.polarsignals.com",
            token_generator=lambda: self.config["bearer_token"],
            relation_name="parca-store-endpoint",
        )

    def _update(self, _):
        """Check that the config provided is valid and set charm status accordingly."""
        if not self.config["bearer_token"]:
            self.unit.status = ops.BlockedStatus("no cloud token configured")
        else:
            self.unit.status = ops.ActiveStatus()


if __name__ == "__main__":
    ops.main(PolarSignalsCloudIntegratorCharm)
