import requests

url = "http://127.0.0.1:5000/verify"

image1 = {'image1': open('/home/raf1n/my_projects/e-kyc/public/4.jpeg', 'rb')}
image2 = {'image2': open('/home/raf1n/my_projects/e-kyc/public/3.jpeg', 'rb')}

response = requests.post(url, files=image1 | image2)
print(response.json())
