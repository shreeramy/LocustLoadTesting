'''
locustfile.py
ModernAging

Created on 11/04/2024 by v.jamlia@crestecusa.com
Copyright (C) 2024 Author Vivek
'''

from locust import HttpUser, task, between
import faker

fake = faker.Faker()

class HealthWellnessUser(HttpUser):
    """Represents a user for load testing health and wellness related APIs."""
    
    wait_time = between(3, 5)
    
    """
    Wait_time makes it easy to introduce delays after each task execution. 
    If no wait_time is specified, the next task will be executed as soon as one finishes.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.signup_credentials = []
        self.user_ids = []

    
    def signup_task(self):
        """
        Task to perform user signup.

        This task generates random username and email using the Faker library, and a fixed password.
        It then sends a signup request to the specified API endpoint with the generated credentials.
        If the signup request is successful (status code 201), it indicates that a new user has been created.
        """

        username = fake.user_name()
        password = "admin@123"

        response = self.client.post(
            "signup/", 
            json={
                "username": username,
                "password": password
            }
        )

        if response.status_code == 201:
            print(f"User {username} with id {response.json()['id']} signed up successfully")
            self.signup_credentials.append((username, password))
        else:
            print(f"Failed to sign up user {username}")

    @task
    def login_task(self):
        """
        This task retrieves the credentials of the last signed-up user and uses them
        to perform a login request. Upon successful login, it extracts the access token
        from the response and sets it in the headers for subsequent API requests.

        If no users have signed up yet, this task will skip the login process.
        """

        if self.signup_credentials:
            username, password = self.signup_credentials[-1]
            response = self.client.post(
                "api/token/", 
                json={
                    "username": username, 
                    "password": password
                }
            )
            if response.status_code == 200:
                self.access_token = response.json().get("access")
                self.headers = {"Authorization": f"Bearer {self.access_token}"}
                # self.user_id = response.json()['user']['id']
                # self.userprofile = response.json()['user']['userprofile']['id']
                print(f"User {username} logged in successfully")
            else:
                print(response.text, f"Failed to log in user")
        else:
            print("No users signed up yet, skipping login")

    @task
    def test_api_with_token(self):
        """
        Task to test various APIs with an authorization token.

        This task sends requests to multiple API endpoints using the access token
        stored in the user instance.
        The requests are sent with the Authorization header containing the access token.
        """
        
        if hasattr(self, "access_token"):
            headers = {"Authorization": f"Bearer {self.access_token}"}

            self.client.get(
                'get-items/',
                headers=headers,
                name="get-items"
            )

            self.client.post(
                'create-items/',
                headers=headers,
                json={
                    'task_name': "tasks"
                },
                name="create-items"
            )            
        else:
            print("User not logged in, skipping API test")

    def on_start(self):
        """
        Method called when a user instance starts running.

        This method is automatically called by Locust when a user instance starts running.
        It performs the signup and login tasks for the user, ensuring that the user is registered
        and logged in before any other tasks are executed.
        """

        self.signup_task()
        self.login_task()

    def on_stop(self):
        """
        Method called when a user instance stops running.

        This method is automatically called by Locust when a user instance stops running.
        It iterates through the list of user IDs stored in the user instance and sends a DELETE request
        to the corresponding API endpoint to delete each user. The requests are sent with the authorization
        token stored in the user instance's headers.

        If the DELETE request is successful (status code 204), it indicates that the user has been deleted.
        If the request fails, an error message is printed.
        """

        response = self.client.get(
            f'delete-user/',
            headers=self.headers,
            name='delete-user'
        )
        if response.status_code == 200:
            print(f"User deleted successfully")
        else:
            print(f"Failed to delete user.")
