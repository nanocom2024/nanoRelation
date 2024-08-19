import requests

token = ''


def test_signup_success(baseurl):
    global token
    url = baseurl+'/signup'
    res = requests.post(url, json={
        'name': 'test',
        'email': 'test@test.org',
        'password': 'password'
    })
    token = res.json()['token']
    assert res.status_code == 200
    assert token


def test_signup_missing_name(baseurl):
    url = baseurl+'/signup'
    res = requests.post(url, json={
        'name': '',
        'email': 'test@test.org',
        'password': 'password'
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Missing name'


def test_signup_missing_email(baseurl):
    url = baseurl+'/signup'
    res = requests.post(url, json={
        'name': 'test',
        'email': '',
        'password': 'password'
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Missing email'


def test_signup_missing_password(baseurl):
    url = baseurl+'/signup'
    res = requests.post(url, json={
        'name': 'test',
        'email': 'test@test.org',
        'password': ''
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Missing password'


def test_signup_already_exist(baseurl):
    url = baseurl+'/signup'
    res = requests.post(url, json={
        'name': 'test',
        'email': 'test@test.org',
        'password': 'password'
    })
    assert res.status_code == 400
    expected = 'The user with the provided email already exists (EMAIL_EXISTS).'
    assert res.json()['error'] == expected


def test_signout_missing_token(baseurl):
    url = baseurl+'/signout'
    res = requests.post(url, json={
        'token': ''
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Invalid token'


def test_signout_invalid_token(baseurl):
    url = baseurl+'/signout'
    res = requests.post(url, json={
        'token': 'invalidToken'
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Invalid token'


def test_signout_success(baseurl):
    global token
    url = baseurl+'/signout'
    res = requests.post(url, json={
        'token': token
    })
    assert res.status_code == 200
    assert res.json() == {'done': 'success'}


def test_signin_success(baseurl):
    global token
    url = baseurl+'/signin'
    res = requests.post(url, json={
        'email': 'test@test.org',
        'password': 'password'
    })
    token = res.json()['token']
    assert res.status_code == 200
    assert token


def test_signin_missing_email(baseurl):
    url = baseurl+'/signin'
    res = requests.post(url, json={
        'email': '',
        'password': 'password'
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Missing email'


def test_signin_missing_password(baseurl):
    url = baseurl+'/signin'
    res = requests.post(url, json={
        'email': 'test@test.org',
        'password': ''
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Missing password'


def test_signin_wrong_email(baseurl):
    url = baseurl+'/signin'
    res = requests.post(url, json={
        'email': 'wrongEmail@test.org',
        'password': 'password'
    })
    assert res.status_code == 400
    expected = 'No user record found for the provided email: wrongEmail@test.org.'
    assert res.json()['error'] == expected


def test_signin_wrong_password(baseurl):
    url = baseurl+'/signin'
    res = requests.post(url, json={
        'email': 'test@test.org',
        'password': 'wrongPassword'
    })
    assert res.status_code == 400
    expected = 'INVALID_LOGIN_CREDENTIALS'
    assert res.json()['error'] == expected


def test_delete_account_missing_password(baseurl):
    global token
    url = baseurl+'/delete_account'
    res = requests.post(url, json={
        'password': '',
        'confirmPassword': 'password',
        'token': token
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Missing password'


def test_delete_account_missing_confirm_password(baseurl):
    global token
    url = baseurl+'/delete_account'
    res = requests.post(url, json={
        'password': 'password',
        'confirmPassword': '',
        'token': token
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Missing confirmPassword'


def test_delete_account_missing_token(baseurl):
    url = baseurl+'/delete_account'
    res = requests.post(url, json={
        'password': 'password',
        'confirmPassword': 'password',
        'token': ''
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Invalid token'


def test_delete_account_passwords_do_not_match(baseurl):
    global token
    url = baseurl+'/delete_account'
    res = requests.post(url, json={
        'password': 'password',
        'confirmPassword': 'wrongPassword',
        'token': token
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Passwords do not match'


def test_delete_account_invalid_token(baseurl):
    url = baseurl+'/delete_account'
    res = requests.post(url, json={
        'password': 'password',
        'confirmPassword': 'password',
        'token': 'invalidToken'
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Invalid token'


def test_delete_account_invalid_password(baseurl):
    global token
    url = baseurl+'/delete_account'
    res = requests.post(url, json={
        'password': 'invalidPassword',
        'confirmPassword': 'invalidPassword',
        'token': token
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'INVALID_LOGIN_CREDENTIALS'


def test_delete_account_success(baseurl):
    global token
    url = baseurl+'/delete_account'

    res = requests.post(url, json={
        'password': 'password',
        'confirmPassword': 'password',
        'token': token
    })
    assert res.status_code == 200
    assert res.json()['done'] == 'success'
