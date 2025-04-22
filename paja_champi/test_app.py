import pytest
from app import app

# Fixture para inicializar el cliente de test de Flask
@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Opcional: desactivar protecciones CSRF u otros si las tienes
    with app.test_client() as client:
        yield client

def test_login_page(client):
    # Verifica que la página de login se carga correctamente
    response = client.get('/login')
    assert response.status_code == 200
    # Puedes verificar que algún texto característico de la página aparezca
    assert b'iniciar sesi' in response.data.lower()  # Busca "iniciar sesión" en minúsculas

def test_protected_endpoint_without_login(client):
    # Intenta acceder a una ruta protegida sin iniciar sesión
    response = client.get('/test_auth', follow_redirects=True)
    # La aplicación debería redirigir a la página de login y mostrar un mensaje de advertencia
    assert b'por favor, inicia sesi' in response.data.lower()

def test_protected_endpoint_with_login(client):
    # Para acceder a rutas protegidas, simulamos que el usuario ha iniciado sesión
    with client.session_transaction() as sess:
        sess['user'] = '1234'
        sess['role'] = 'recepcion'
    response = client.get('/test_auth')
    assert response.status_code == 200
    # Verifica que el mensaje de la ruta protegida incluya el código de usuario
    assert b'user 1234' in response.data.lower()
