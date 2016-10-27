import fast_paxos

app = fast_paxos.app.test_client()


def test_sample():
    assert 2 + 2 == 4


def test_response():
    response = app.get('/')
    assert b'Hello World!' in response.data
