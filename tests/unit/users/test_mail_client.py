import pytest
from app.users.auth.client.mail import MailClient


class FakeTask:
    def __init__(self):
        self.calls = []

    def delay(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        return None


def test_mailclient_send_welcome(monkeypatch):
    fake = FakeTask()
    monkeypatch.setattr('app.users.auth.client.mail.send_email_task', fake)

    MailClient.send_welcome_email('test@mail')

    assert len(fake.calls) == 1
    args, kwargs = fake.calls[0]
    assert args[0] == 'Welcome email'
    assert 'Welcome to pomodoro' in args[1]
    assert args[2] == 'test@mail'
