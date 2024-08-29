# Copyright 2023 Jon Seager
# See LICENSE file for licensing details.

import asyncio

from pytest import mark
from pytest_operator.plugin import OpsTest

PSCLOUD = "polar-signals-cloud"


@mark.abort_on_fail
async def test_deploy(ops_test: OpsTest, charm_under_test):
    charm = await charm_under_test
    await asyncio.gather(
        ops_test.model.deploy(
            charm,
            application_name=PSCLOUD,
            config={"bearer_token": "deadbeef"},
            series="jammy",
        ),
        ops_test.model.wait_for_idle(
            apps=[PSCLOUD], status="active", raise_on_blocked=True, timeout=1000
        ),
    )


@mark.abort_on_fail
async def test_profile_store_relation(ops_test: OpsTest):
    await asyncio.gather(
        ops_test.model.deploy(
            "ubuntu-lite",
            channel="stable",
            series="jammy",
            constraints={"virt-type": "virtual-machine"},
        ),
        ops_test.model.deploy("parca-agent", channel="edge", num_units=0, series="jammy"),
        ops_test.model.wait_for_idle(
            apps=["ubuntu-lite"],
            status="active",
            raise_on_blocked=True,
            timeout=1000,
        ),
    )
    await asyncio.gather(
        ops_test.model.integrate("ubuntu-lite", "parca-agent"),
        ops_test.model.integrate(PSCLOUD, "parca-agent"),
        ops_test.model.wait_for_idle(
            apps=[PSCLOUD, "parca-agent"],
            status="active",
            raise_on_blocked=True,
            timeout=1000,
        ),
    )
