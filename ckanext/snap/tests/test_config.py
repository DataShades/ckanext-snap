"""Tests for ckanext.snap.config.

You don't have to write tests for this module, unless it does something
complex.
"""

import pytest

from ckanext.snap import config



@pytest.mark.skip
class TestMultivalued:
    """Test multivalued() accessor."""

    def test_default(self):
        """Default option is available."""
        assert config.multivalued() == []

    @pytest.mark.ckan_config(config.TRACKED_ACTIONS, [1, 2, 3])
    def test_modified(self):
        """Modified option is available."""
        assert config.multivalued() == [1, 2, 3]
