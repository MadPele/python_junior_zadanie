from app import configure_routes
from flask import Flask

# Before run tests please delete "task_list" file from project folder


def test_base_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/'

    response = client.get(url)
    assert response.get_data() == b'Hello World!'
    assert response.status_code == 200


def test_user_task_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/app/5'

    response = client.get(url)
    assert b'Name' in response.get_data()
    assert b'City' in response.get_data()
    assert b'Task' in response.get_data()
    assert b'Completed' in response.get_data()
    assert response.status_code == 200


def test_print_all_route_without_file():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/app/printall'

    response = client.get(url)
    assert b'You need to download file first' in response.get_data()
    assert response.status_code == 200


def test_create_file_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/app/all'

    response = client.get(url)
    assert b'Saved' in response.get_data()
    assert response.status_code == 200


def test_print_all_route_with_file():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/app/printall'

    response = client.get(url)
    assert b'Read' in response.get_data()
    assert response.status_code == 200


