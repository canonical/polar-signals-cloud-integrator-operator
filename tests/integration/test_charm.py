# Copyright 2023 Jon Seager
# See LICENSE file for licensing details.

import pytest
from conftest import APP_BASE, APP_NAME, COS_CHANNEL
from jubilant import Juju, all_active, any_error

PARCA_AGENT_APP_NAME = "parca-agent"
UBUNTU_LITE_APP_NAME = "ubuntu-lite"


@pytest.mark.setup
def test_deploy(juju: Juju, charm):
    juju.deploy(charm, APP_NAME, config={"bearer_token": "deadbeef"})
    juju.wait(all_active, timeout=5 * 60, error=any_error, delay=10, successes=3)


@pytest.mark.setup
def test_deploy_profile_store(juju: Juju):
    juju.deploy(
        UBUNTU_LITE_APP_NAME,
        channel="stable",
        base=APP_BASE,
        constraints={"virt-type": "virtual-machine"},
    )
    juju.deploy(PARCA_AGENT_APP_NAME, channel=COS_CHANNEL, num_units=0, base=APP_BASE)
    juju.wait(
        lambda status: all_active(status, UBUNTU_LITE_APP_NAME),
        timeout=5 * 60,
        error=any_error,
        delay=10,
        successes=3,
    )


@pytest.mark.abort_on_fail
def test_integrate_profile_store(juju: Juju):
    juju.integrate(UBUNTU_LITE_APP_NAME, PARCA_AGENT_APP_NAME)
    juju.integrate(APP_NAME, PARCA_AGENT_APP_NAME)
    juju.wait(
        lambda status: all_active(status, APP_NAME, PARCA_AGENT_APP_NAME),
        timeout=5 * 60,
        error=any_error,
        delay=10,
        successes=3,
    )
