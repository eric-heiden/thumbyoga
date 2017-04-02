import os, requests, cv2, base64, json
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

# select buckets as per timestamp
buck = []
# buck.append( None )
buck.append( ClarifaiApp("V9eiZZRUExkv5fRgno2DxvvG5fJfz3ICM-zuLrhR", "kKind6PH-zYg6FIKOtuD_IK-kFJKjmsgK9hFkavy") )
buck.append( ClarifaiApp("8Ql2EnIC5dgx02HkORIlRlAseAASuwiuHRrty50v", "_DiEG9gEGmP7luHcitUOQpJRS-fvxlfLXbZFYiIw") )
buck.append( ClarifaiApp("u7pOW9u4HRUoEhTqYhw6D6Z_he45FPSiGV8odDIv", "2BU18_hN2AW1nPlOdHeH6f3aDmranIMWJ1pmW4AH") )
buck.append( ClarifaiApp("diDr3Nv2Fa-EhbBROYbg8Ic8iyUVCZ4wL98tKutP", "TVHhYtjTmQGWnXLzQS6xB62bi1Me59muQnK1aBt4") )
buck.append( ClarifaiApp("DRLD8ieb2xiJvhPYbc9cPBGpFq3XBKbXfc6aDhow", "mri66cHqJLZHk5XVF4JyUnRPDaF5Gy7qUmpe6EEf") )

buckId = 4

def processRequest( jsonData, data, headers, params ):
    """
    Helper function to process the request to Project Oxford

    Parameters:
    jsonData: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    url = 'https://westus.api.cognitive.microsoft.com/vision/v1.0/generateThumbnail'

    while True:

        response = requests.request( 'post', url, json = jsonData, data = data, headers = headers, params = params )

        if response.status_code == 429: 

            print( "Message: %s" % ( response.json()['error']['message'] ) )

            if retries <= _maxNumRetries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print( 'Error: failed after retrying!' )
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
                result = None 
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
                if 'application/json' in response.headers['content-type'].lower(): 
                    result = response.json() if response.content else None 
                elif 'image' in response.headers['content-type'].lower(): 
                    result = response.content
        else:
            print( "Error code: %d" % ( response.status_code ) )
            # print( "Message: %s" % ( response.json() ) )

        break
        
    return result


# Circular buffer
def increment(lastBucketId):
    print("Incrementing bucket id %i" % lastBucketId)
    return (lastBucketId+1) % 5
    # if(lastBucketId == 5):
    #     return 1
    # else:
    #     return lastBucketId+1


def getNextBucket(lastBucketId, lastTimestamp, imgTimestamp):
    global buckId

    buckId = lastBucketId

    if (lastTimestamp - imgTimestamp).total_seconds() > 2:
        buckId = increment(lastBucketId)

    return buckId


# Initialize the Flask application
app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    if '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']:
        return filename.rsplit('.', 1)[1]
    else:
        return False

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('index.html')


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename) != False:
        # Make the filename safe, remove unsupported chars
        extension = allowed_file(file.filename)
        filename = "tempory.%s" % extension

        target_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        with Image.open(file) as img:
            img_exif = img._getexif()
            if img_exif is not None and len(img_exif) > 36867:
                dt = img_exif[36867]
                print('Date', dt)
                dt = datetime.strptime(dt, '%Y:%m:%d %H:%M:%S')
            else:
                print('Could not find EXIF tag for time stamp of capture. Resorting to file creation time stamp.')
                dt = datetime.now()
            # crop image
            img.thumbnail([1500, 1500], Image.ANTIALIAS) #resizeimage.resize_thumbnail(img, [1500, 1500])
            # img.save('uploads/temp.jpg')
            filename = "%s.%s" % (dt.strftime('%Y%m%d%H%M%S'), extension)
            target_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img.save(target_filename, img.format)

        # Load raw image file into memory
        with open(target_filename, 'rb') as f:
            data = f.read()
            
        # Computer Vision parameters
        params = {
            "width": 700,
            "height": 700,
            "smartCropping": True
        } 

        headers = dict()
        headers['Ocp-Apim-Subscription-Key'] = _key
        headers['Content-Type'] = 'application/octet-stream'

        print("Generating smart thumbnail...")
        result = processRequest(None, data, headers, params)

        # update buckets
        bucket = db.Bucket.find_one()
        buckId = getNextBucket(bucket['lastBucketId'], bucket['lastTimestamp'], dt)

        if buckId != bucket['lastBucketId']:
            buck[ buckId ].deleteAll()
            db.Bucket.update(
                {
                    _id: bucket._id
                },
                {
                    '$set': {'lastBucketId': buckId, 'lastTimestamp': dt}
                }
            )


        b64data = None
        if result is not None:
            # print(result)
            print("Saving smart thumbnail...")
            # Load the original image, fetched from the URL
            data8uint = np.fromstring(result, np.uint8) # Convert string to an unsigned int array
            img = cv2.imdecode(data8uint, cv2.IMREAD_COLOR) #cv2.cvtColor(cv2.imdecode(data8uint, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
            cv2.imwrite(target_filename, img, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
            with open(target_filename, 'rb') as f:
                data = f.read()
                b64data = base64.b64encode(data)
                image_id = str(db.Image.count() + 1)
                image = buck[ buckId ].inputs.create_image_from_base64(b64data)
        else:
            print('Error while computing smart thumbnails.')


        # TODO construct output JSON
        # search for all similar images
        bucket_results = []
        for i in range(5):
            result = buck[i].inputs.search_by_image(base64bytes=b64data)
            # print('SEARCH_BY_IMAGE Result', result)
            # print('Hits', result["hits"])

            bucket_results.append([res.url for res in result[:min(len(result), 3)]])

            # count = 0
            # for img in simImg:
            #     count = count +1
            #     # json += json_encode(img)

            #     if count == 3:
            #         break

        return json.dumps({ "bucket_results": bucket_results })

        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file

        # return redirect(url_for('uploaded_file',
        #                         filename=filename))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("5000"),
        debug=True
    )
