import requests
import io

def download_image(url):
    response = requests.get(url)
    return io.BytesIO(response.content)

image1_url = 'https://s3.brilliant.com.bd/face-verification-images/img_2.png'
image2_url = 'https://s3.brilliant.com.bd/face-verification-images/5.jpg'

image1 = download_image(image1_url)
image2 = download_image(image2_url)

url = "http://103.209.42.222:8000/verify_faces_async"

response = requests.post(url, files={'image1': image1, 'image2': image2})

print(response.json())


url = "http://127.0.0.1:8000/verify_faces_async"