from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def get_tasks(self):
        self.client.get("/api/tasks")

    @task(1)
    def create_task(self):
        self.client.post("/api/tasks", json={
            "title": "A new load testing task",
            "completed": False
        })
