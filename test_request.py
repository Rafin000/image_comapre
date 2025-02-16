import requests

url = "http://127.0.0.1:8000/verify"

image1 = {'image1': open('/home/raf1n/my_projects/e-kyc/public/1.jpeg', 'rb')}
image2 = {'image2': open('/home/raf1n/my_projects/e-kyc/public/2.jpeg', 'rb')}

response = requests.post(url, files=image1 | image2)
print(response.json())
