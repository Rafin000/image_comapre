# locustfile.py
from locust import HttpUser, task, between
import os
import time

class FaceVerificationUser(HttpUser):
    wait_time = between(1, 2)  

    @task
    def verify_faces(self):
        # Submit verification task
        url = "/verify_faces_async"  
        image1_path = "/home/raf1n/my_projects/e-kyc/public/1.jpeg" 
        image2_path = "/home/raf1n/my_projects/e-kyc/public/2.jpeg"

        if not os.path.exists(image1_path) or not os.path.exists(image2_path):
            print("Test images not found!")
            return

        with open(image1_path, "rb") as img1, open(image2_path, "rb") as img2:
            files = {
                "image1": (os.path.basename(image1_path), img1, "image/jpeg"),
                "image2": (os.path.basename(image2_path), img2, "image/jpeg"),
            }
            response = self.client.post(url, files=files)

        if response.status_code == 200:
            task_data = response.json()
            task_id = task_data.get("task_id")
            print(f"Task submitted: {task_id}")
            
            # Optional: Poll for results
            self.poll_for_results(task_id)
        else:
            print(f"Failed to submit task: {response.status_code}, {response.text}")
    
    def poll_for_results(self, task_id):
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
            time.sleep(2)  # Wait 2 seconds between polls