# Copyright 2023 Jon Seager.
# See LICENSE file for licensing details.

import unittest

from charm import PolarSignalsCloudIntegratorCharm
from ops.model import ActiveStatus, BlockedStatus
from ops.testing import Harness


class TestCharm(unittest.TestCase):
    def setUp(self):
        self.harness = Harness(PolarSignalsCloudIntegratorCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.set_leader(True)
        self.harness.begin()
        self.maxDiff = None

    def test_charm_blocks_if_no_token_specified(self):
        self.harness.update_config({"bearer_token": ""})
        self.assertEqual(
            self.harness.model.unit.status,
            BlockedStatus("no cloud token configured"),
        )

    def test_charm_sets_relation_data_for_valid_token(self):
        self.harness.update_config({"bearer_token": "deadbeef"})

        self.assertEqual(self.harness.model.unit.status, ActiveStatus())

        rel_id = self.harness.add_relation("parca-store-endpoint", "parca-agent")
        relation_data = self.harness.get_relation_data(rel_id, self.harness.charm.app.name)
        self.harness.add_relation_unit(rel_id, "parca-agent/0")

        expected = {
            "remote-store-address": "gprc.polarsignals.com:443",
            "remote-store-bearer-token": "deadbeef",
            "insecure": "false",
        }

        self.assertEqual(expected, relation_data)

    def test_non_leader_does_not_modify_relation_data(self):
        self.harness.set_leader(False)
        self.harness.update_config({"bearer_token": "foobar"})
        rel_id = self.harness.add_relation("parca-store-endpoint", "parca-agent")
        relation_data = self.harness.get_relation_data(rel_id, self.harness.charm.app.name)
        self.assertEqual({}, relation_data)

    def test_charm_removes_token_when_blank(self):
        self.harness.update_config({"bearer_token": "deadbeef"})

        self.assertEqual(self.harness.model.unit.status, ActiveStatus())

        rel_id = self.harness.add_relation("parca-store-endpoint", "parca-agent")
        relation_data = self.harness.get_relation_data(rel_id, self.harness.charm.app.name)
        self.harness.add_relation_unit(rel_id, "parca-agent/0")

        expected = {
            "remote-store-address": "gprc.polarsignals.com:443",
            "remote-store-bearer-token": "deadbeef",
            "insecure": "false",
        }

        self.assertEqual(expected, relation_data)

        self.harness.update_config({"bearer_token": ""})

        self.assertIsInstance(self.harness.model.unit.status, BlockedStatus)

        self.assertEqual(dict(relation_data).get("remote-store-bearer-token", ""), "")
