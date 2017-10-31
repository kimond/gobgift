import json
import pytest

pytestmark = pytest.mark.django_db


def create_test_file(path):
    f = open(path, 'w')
    f.write('test123\n')
    f.close()
    f = open(path, 'rb')
    return f


@pytest.mark.skip()
def test_upload_gift_photo_through_rest(logged_client):
    url = '/api/gifts/'
    file = create_test_file('/tmp/photo.png')

    response = logged_client.post(url, data={"photo": file}, content_type='multipart/form-data')

    print(response.content)
    assert response.status_code == 201
