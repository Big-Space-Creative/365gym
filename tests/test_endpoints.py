def test_home_page_returns_200(client, settings):
    """Comprova que / responde 200 no runserver com DEBUG=True (boas-vindas do Django)."""
    settings.DEBUG = True
    response = client.get("/", HTTP_HOST="127.0.0.1")
    assert response.status_code == 200


def test_admin_login_returns_200(client):
    """Comprova que /admin/login/ responde 200."""
    response = client.get("/admin/login/", HTTP_HOST="127.0.0.1")
    assert response.status_code == 200
