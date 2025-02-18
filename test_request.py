#test_request.py
import requests

url = "http://127.0.0.1:8000/verify_faces_async"

with open('/home/raf1n/my_projects/e-kyc/public/1.jpeg', 'rb') as image1, \
     open('/home/raf1n/my_projects/e-kyc/public/2.jpeg', 'rb') as image2:

    response = requests.post(url, files={'image1': image1, 'image2': image2})
    print(response.json())
