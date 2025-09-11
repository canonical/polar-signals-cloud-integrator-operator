# Copyright 2023 Jon Seager.
# See LICENSE file for licensing details.
import os
from pathlib import Path

import pytest
import yaml
from pytest_jubilant import pack

APP_NAME = "polar-signals-cloud"
METADATA = yaml.safe_load(Path("./charmcraft.yaml").read_text())
APP_BASE = next(iter(METADATA["platforms"])).split(":")[0]
COS_CHANNEL = "2/edge"


@pytest.fixture(scope="module")
def charm():
    if charm_file := os.environ.get("CHARM_PATH"):
        return Path(charm_file)
    return pack(".")
