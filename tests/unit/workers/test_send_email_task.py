from worker.celery import send_email_task, _build_message


def test_build_message():
    subj = "Test"
    text = "Hello"
    to = "user@example.com"

    msg = _build_message(subj, text, to)

    assert msg['Subject'] == subj
    assert msg['To'] == to
    assert msg.get_payload()[0].get_payload() == text


def test_send_email_task_calls_send(monkeypatch):
    called = {}

    def fake_send(msg):
        called['msg'] = msg

    monkeypatch.setattr('worker.celery._send_email', fake_send)

    send_email_task.run('Hi', 'Body', 't@example.com')

    assert 'msg' in called
    assert called['msg']['To'] == 't@example.com'
