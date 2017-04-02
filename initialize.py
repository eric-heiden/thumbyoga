import os, requests, cv2, base64
from PIL import Image
from resizeimage import resizeimage
from dateutil import parser
from datetime import datetime
import numpy as np
from pymongo import MongoClient

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
from clarifai.rest import ClarifaiApp

_url = 'https://westus.api.cognitive.microsoft.com/vision/v1.0/generateThumbnail'
_key = 'afb83eda55b94d7dbdf3a4c6d23bf3df'

client = MongoClient('mongodb://thumbyoga:V2QhIdJ7YpBvSxYuKsw0xCWkKoVoQFL55OAXt6dLUc97ZdXEBQQYFbnnvcdQORyYspPYJlusaq0PC1njpzcofQ==@thumbyoga.documents.azure.com:10250/?ssl=true')
db = client.thumbyoga

db.Bucket.delete_many({})
# db.Image.delete_many({})

db.Bucket.insert_one({'lastBucketId': 4, 'lastTimestamp': datetime.now()})

buck = []
# buck.append( None )
buck.append( ClarifaiApp("V9eiZZRUExkv5fRgno2DxvvG5fJfz3ICM-zuLrhR", "kKind6PH-zYg6FIKOtuD_IK-kFJKjmsgK9hFkavy") )
buck.append( ClarifaiApp("8Ql2EnIC5dgx02HkORIlRlAseAASuwiuHRrty50v", "_DiEG9gEGmP7luHcitUOQpJRS-fvxlfLXbZFYiIw") )
buck.append( ClarifaiApp("u7pOW9u4HRUoEhTqYhw6D6Z_he45FPSiGV8odDIv", "2BU18_hN2AW1nPlOdHeH6f3aDmranIMWJ1pmW4AH") )
buck.append( ClarifaiApp("diDr3Nv2Fa-EhbBROYbg8Ic8iyUVCZ4wL98tKutP", "TVHhYtjTmQGWnXLzQS6xB62bi1Me59muQnK1aBt4") )
buck.append( ClarifaiApp("DRLD8ieb2xiJvhPYbc9cPBGpFq3XBKbXfc6aDhow", "mri66cHqJLZHk5XVF4JyUnRPDaF5Gy7qUmpe6EEf") )

for b in buck:
	b.deleteAll()