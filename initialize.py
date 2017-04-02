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
db.Image.delete_many({})

db.Bucket.insert_one({'lastBucketId': 4, 'lastTimestamp': datetime.now()})