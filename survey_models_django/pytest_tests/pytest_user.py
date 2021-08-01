import pytest


from django.contrib.auth import get_user_model


@pytest.fixture
def User():    
    User = get_user_model()
    return User

@pytest.fixture
def test_user():    
    user = get_user_model().objects.create_user(
        username='testname',
        password='testpassword'
    )
    return user

@pytest.mark.django_db
def test_std_create_user():
    User = get_user_model()
    user = User.objects.create_user(
        username='testname',
        password='testpassword'
    )
    assert user.username == 'testname'
    assert user.is_active == True
    assert user.is_staff == False
    assert user.is_superuser == False

@pytest.mark.django_db
def test_custom_create_user(client, User):
    test_name = "Ivan"
    resp = client.post('/auth/register/', data={"username": test_name,
                                           "password1": "12password12",
                                           "password2": "12password12"})
    assert resp.status_code == 302                                           
    user = User.objects.get(username=test_name)
    assert user.username == test_name
    assert user.is_active == True
    assert user.is_staff == False
    assert user.is_superuser == False

def test_register_user_page(client):
    resp = client.get('/auth/register/')
    assert resp.status_code == 200
    assert 'users/register.html' in (t.name for t in resp.templates)

def test_login_user_page(client):
    resp = client.get('/auth/login/')
    assert resp.status_code == 200
    assert 'users/login.html' in (t.name for t in resp.templates)

@pytest.mark.django_db    
def test_login_correct(client, test_user):    
    response = client.post('/auth/login/', data={'username': 'testname',
                                                 'password': 'testpassword'})
    assert response.status_code == 302

@pytest.mark.django_db    
def test_logout(client):
    client.post('/auth/login/', data={'username': 'testname',
                                      'password': 'testpassword'})
    resp = client.get('/auth/logout/')
    assert resp.status_code == 302

