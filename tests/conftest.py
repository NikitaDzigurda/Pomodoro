import asyncio

import pytest

pytest_plugins = [
    'tests.fixtures.auth.auth_service',
    'tests.fixtures.auth.client',
    'tests.fixtures.users.users_repository',
    'tests.fixtures.infrastructure',
    'tests.fixtures.users.user_model'
]


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
