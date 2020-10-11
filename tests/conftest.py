import socket 

import pytest 


class DisableNetworkConnection(socket.socket):
    def __init__(self, *args, **kwargs):
        raise Exception('Network connection is disabled in test mode.')


socket.socket = DisableNetworkConnection


@pytest.fixture
def load_raw_tx():
    def func(fixture_name):
        filename = f'tests/fixtures/{fixture_name}'
        with open(filename) as f:
            return f.read().strip()
    return func
