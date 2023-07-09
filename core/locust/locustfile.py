from locust import HttpUser, task

from factories.accounts import UserFactory

class QuickStartUser(HttpUser):
    base_url = 'api/v1.0'

    def on_start(self):
        user = UserFactory()
        response = self.client.post(f'{self.base_url}/accounts/jwt/generate', data={"email":user.email, "password":user.password}).json()
        
        self.client.headers = { 'Authorization': f'Bearer {response.get("access", None)}' }

    @task
    def post_list(self):
        self.client.get(f'{self.base_url}/tasks')