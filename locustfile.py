import time
from locust import HttpUser, task, between
import requests
import io

class FaceVerificationUser(HttpUser):
    wait_time = between(1, 2)  

    @task
    def verify_faces(self):
        url = "http://103.209.42.222:8000/verify_faces_async"

        # Fetch images from URLs
        image1_url = 'https://s3.brilliant.com.bd/face-verification-images/img_2.png'
        image2_url = 'https://s3.brilliant.com.bd/face-verification-images/5.jpg'
        
        image1_bytes = self.download_image(image1_url)
        image2_bytes = self.download_image(image2_url)

        if not image1_bytes or not image2_bytes:
            print("Failed to download one or both images.")
            return

        # Prepare multipart/form-data payload
        files = {
            "image1": ("image1.jpg", image1_bytes, "image/jpeg"),
            "image2": ("image2.jpg", image2_bytes, "image/jpeg"),
        }

        response = self.client.post(url, files=files)

        if response.status_code == 200:
            task_data = response.json()
            task_id = task_data.get("task_id")
            print(f"Task submitted: {task_id}")
            self.poll_for_results(task_id)
        else:
            print(f"Failed to submit task: {response.status_code}, {response.text}")

    def poll_for_results(self, task_id):
        """Poll the server to get the result of the verification task."""
        max_attempts = 5
        attempts = 0

        while attempts < max_attempts:
            result_response = self.client.get(f"/task_result/{task_id}")

            if result_response.status_code == 200:
                result_data = result_response.json()
                status = result_data.get("status")

                if status == "completed":
                    print(f"Task completed: {result_data.get('result')}")
                    return
                print(f"Task still processing, attempt {attempts+1}/{max_attempts}")
            else:
                print(f"Failed to get result: {result_response.status_code}")
                return

            attempts += 1
            time.sleep(2) 

    def download_image(self, url):
        """Download an image from a given URL and return its bytes."""
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return io.BytesIO(response.content)
            print(f"Failed to download image from {url}: {response.status_code}")
        except Exception as e:
            print(f"Error downloading image from {url}: {e}")
        return None
