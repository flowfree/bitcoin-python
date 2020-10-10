import pytest 


@pytest.fixture
def load_raw_tx():
    def func(fixture_name):
        filename = f'tests/fixtures/{fixture_name}'
        with open(filename) as f:
            return f.read().strip()
    return func
