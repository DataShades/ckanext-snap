"""Tests for ckanext.snap.logic.action."""

import pytest
from faker import Faker

from ckan import model
from ckan.tests.helpers import call_action

from ckanext.snap.model import Snapshot

@pytest.mark.ckan_config("ckan.plugins", "snap")
@pytest.mark.usefixtures("with_plugins")
def test_snapshot_create(faker: Faker):
    """Snapshot is created."""
    hello = faker.word()
    world = faker.word()

    # action tests use `call_action` to skip authorization check. All auth
    # functions are checked separately.
    result = call_action(
        "snap_snapshot_create",
        hello=hello,
        world=world,
    )

    # if validation covered by schema, do not verify it inside action
    # test. Basically, test the result of action, not it's internal
    # implementation details.
    assert result["hello"] == hello
    assert result["world"] == world

    smth = model.Session.get(Snapshot, result["id"])
    assert smth.hello == hello
