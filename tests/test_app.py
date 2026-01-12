def test_home(client):
    response = client.get('/')

    assert b'<title>App ejemplo</title>' in response.data


def test_create_client(client):
    from app.models import Client

    init_session(client)

    post_data = { 'name': 'Admin', 'address': 'Test addr'}
    
    response = client.post('/clients/create', data=post_data)

    cl = Client.query.filter(Client.name == 'Admin').first()

    assert response.status_code == 302
    assert cl is not None
    assert cl.name == 'Admin'


def test_delete_client(client):
    from app.models import Client
    from app.database import db_session

    init_session(client)

    cl = Client()
    cl.name = 'Admin'

    db_session.add(cl)
    db_session.commit()

    response = client.post('/clients/delete/' + str(cl.id))

    cl = db_session.get(Client, cl.id)

    assert response.status_code == 302
    assert cl is None


def init_session(client):
    with client.session_transaction() as session:
        session['user_id'] = 1
