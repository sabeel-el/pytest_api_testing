import requests
import pytest
import json
import csv



def write_to_csv(request_type, response_status, test, result):
    with open('results.csv', mode='a', newline='') as res:
        writer = csv.writer(res)
        # Write header if file is empty
        if res.tell() == 0:
            writer.writerow(['Request Type', 'Test', 'Response Status', 'Result'])
        writer.writerow([request_type, test, response_status, result])

@pytest.fixture
def base_url():
    return "https://jsonplaceholder.typicode.com"

@pytest.fixture
def data():
    with open('test_data.json', 'r', encoding='utf-8') as file:
        return json.load(file)

class TestJSONPlaceholderAPI:

    def test_get_status(self, base_url):
        endpoint=f"{base_url}/posts"
        response = requests.get(endpoint)
        try:
            assert response.status_code == 200
            write_to_csv('GET', response.status_code, 'get_status', 'Passed')
        except AssertionError:
            write_to_csv('GET', response.status_code, 'get_status', 'Failed')

    def test_get_response_type(self,base_url):
        response = requests.get(f"{base_url}/posts")
        try:
            assert isinstance(response.json(), list)
            write_to_csv('GET', response.status_code, 'response_type', 'Passed')
        except AssertionError:
            write_to_csv('GET', response.status_code, 'response_type', 'Failed')

    def test_get_response_length(self,base_url):
        response = requests.get(f"{base_url}/posts")
        try:
            assert len(response.json()) > 0, "No posts returned"
            write_to_csv('GET', response.status_code, 'response_length', 'Passed')
        except AssertionError:
            write_to_csv('GET', response.status_code, 'response_length', 'Failed')



    def test_get_post_type(self, base_url):
        post_id = 1
        response = requests.get(f"{base_url}/posts/{post_id}")
        post = response.json()
        try:
            assert isinstance(post, dict)
            write_to_csv('GET', response.status_code, 'post_type', 'Passed')
        except AssertionError:
            write_to_csv('GET', response.status_code, 'post_type', 'Failed')


    def test_get_post_count(self, base_url):
        post_id = 1
        response = requests.get(f"{base_url}/posts")
        posts = response.json()
        try:
            assert len(posts)==100
            write_to_csv('GET', response.status_code, 'posts_count', 'Passed')
        except AssertionError:
            write_to_csv('GET', response.status_code, 'posts_count', 'Failed')


    #'''-----------------------------------POST-------------------------------------------------'''
        
    def test_post_status(self, base_url,data):
        payload=data[1]
        response = requests.post(f"{base_url}/posts", json=payload)
        try:
            assert response.status_code == 201
            write_to_csv('POST', response.status_code, 'status', 'Passed')
        except AssertionError:
            write_to_csv('POST', response.status_code, 'status', 'Failed')

        

    def test_post_id_present(self, base_url,data):
        payload = data[2]
        response = requests.post(f"{base_url}/posts", json=payload)
        created_post = response.json()
        try:
            assert "id" in created_post
            write_to_csv('POST', response.status_code, 'id_present', 'Passed')
        except AssertionError:
            write_to_csv('POST', response.status_code, 'id_present', 'Failed')


    def test_post_title(self, base_url,data):
        payload = data[0]
        response = requests.post(f"{base_url}/posts", json=payload)
        created_post = response.json()
        try:
            assert created_post["title"] == payload["title"]
            write_to_csv('POST', response.status_code, 'post_title', 'Passed')
        except AssertionError:
            write_to_csv('POST', response.status_code, 'post_title', 'Failed')
  
    def test_post_header(self, base_url,data):
        payload = data[0]
        response = requests.post(f"{base_url}/posts", json=payload)
        try:
            assert response.headers["Content-Type"] == "application/json; charset=utf-8"  
            write_to_csv('POST', response.status_code, 'content-type', 'Passed')
        except AssertionError:
            write_to_csv('POST', response.status_code, 'content-type', 'Failed')
  
    
    #'''-----------------------------------PUT-------------------------------------------------'''

    def test_put_update_post(self, base_url,data):
        post_id = 4
        payload = data[1]
        response = requests.put(f"{base_url}/posts/{post_id}", json=payload)
        updated_post = response.json()
        try:
            assert updated_post["title"] == payload["title"]
            write_to_csv('PUT', response.status_code, 'updated_title', 'Passed')
        except AssertionError:
            write_to_csv('PUT', response.status_code, 'updated_title', 'Failed')

    def test_put_post_id(self, base_url,data):
        post_id = 1
        payload = data[1]
        response = requests.put(f"{base_url}/posts/{post_id}", json=payload)
        post = response.json()
        try:
            assert post["id"] == post_id
            write_to_csv('PUT', response.status_code, 'post_id', 'Passed')
        except AssertionError:
            write_to_csv('PUT', response.status_code, 'post_id', 'Failed')

    def test_put_authorization(self, base_url,data):
        post_id = 1
        payload = data[1]
        response = requests.put(f"{base_url}/posts/{post_id}", json=payload)
        try:
            assert "Authorization" in response.headers 
            write_to_csv('PUT', response.status_code, 'Authorization', 'Passed')
        except AssertionError:
            write_to_csv('PUT', response.status_code, 'Authorization', 'Failed')

    def test_put_cookies(self, base_url,data):
        post_id = 1
        payload = data[1]
        response = requests.put(f"{base_url}/posts/{post_id}", json=payload)
        try:
            assert "session_id" in response.cookies  
            write_to_csv('PUT', response.status_code, 'cookies', 'Passed')
        except AssertionError:
            write_to_csv('PUT', response.status_code, 'cookies', 'Failed')

    def test_put_response_keys(self, base_url,data):
        post_id = 1
        payload = data[1]
        response = requests.put(f"{base_url}/posts/{post_id}", json=payload)
        res=response.json()
        try:
            assert set(res.keys()) == {"id", "title", "body", "userId"}
            write_to_csv('PUT', response.status_code, 'keys', 'Passed')
        except AssertionError:
            write_to_csv('PUT', response.status_code, 'keys', 'Failed')



    #'''-----------------------------------DELETE-------------------------------------------------'''

    def test_delete_post(self, base_url):
        """Test deleting a post"""
        post_id = 1
        response = requests.delete(f"{base_url}/posts/{post_id}")
        try:
            assert response.text == "{}"
            write_to_csv('DELETE', response.status_code, 'response_text', 'Passed')
        except AssertionError:
            write_to_csv('DELETE', response.status_code, 'response_text', 'Failed')


    def test_delete_response_time(self,base_url):
        post_id=2
        response = requests.delete(f"{base_url}/posts/{post_id}")
        try:
            assert response.elapsed.total_seconds() < 2  
            write_to_csv('DELETE', response.status_code, 'response_time', 'Passed')
        except AssertionError:
            write_to_csv('DELETE', response.status_code, 'response_time', 'Failed')


    def test_delete_content_type(self,base_url):
        post_id=2
        response = requests.delete(f"{base_url}/posts/{post_id}")
        try:
            assert response.headers["Content-Type"] == "application/json; charset=utf-8"  
            write_to_csv('DELETE', response.status_code, 'Content-Type', 'Passed')
        except AssertionError:
            write_to_csv('DELETE', response.status_code, 'Content-Type', 'Failed')

