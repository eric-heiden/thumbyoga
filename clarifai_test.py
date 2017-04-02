# from clarifai import rest
from clarifai.rest import ClarifaiApp
import base64, json

app = ClarifaiApp("V9eiZZRUExkv5fRgno2DxvvG5fJfz3ICM-zuLrhR", "kKind6PH-zYg6FIKOtuD_IK-kFJKjmsgK9hFkavy")
# add image from base64 encoded image bytes
raw_bytes = open("1.jpg", "rb").read()
base64_bytes = base64.b64encode(raw_bytes)
result = app.inputs.create_image_from_base64(base64_bytes)
print(result.url)

# search by base64 bytes
res = app.inputs.search_by_image(url=result.url)
print [r.url for r in res]