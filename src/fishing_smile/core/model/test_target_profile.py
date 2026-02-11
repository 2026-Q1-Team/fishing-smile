import pytest

from .target_profile import TargetProfile

def test_create_with_defaults():
    # TODO: This test is just an example.
    # We should be testing important observable behaviour
    # rather than minor implementation details.
    profile = TargetProfile(
        name = 'John Snow',
        email = 'john.snow@nowhere.westeros.org',
    )
    assert profile.id == None
    assert profile.name == 'John Snow'
    assert profile.phone_number == None

# TODO: test lookup()
