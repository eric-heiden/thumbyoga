import httplib, urllib, base64
import os, requests, cv2, base64
import cognitive_face as CF

body = {
	"url":"http://media.npr.org/assets/img/2017/03/24/soccer_wide-7e96e559fdace2d6a0329da73c38c76fd7bf2c29-s400-c85.jpg"
}


def processRequest(json, data, headers, params, url):
    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:

        response = requests.request( 'post', url, json = json, data = data, headers = headers, params = params )

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
            print( "Message: %s" % ( response.json() ) )

        break
        
    return result

def tagGenerate():
	imageTags = processRequest(body, {}, 
	{#Header
		'Content-Type': 'application/json',
	    'Ocp-Apim-Subscription-Key': '72608f3be7934eaeb9ea0ecf60e585da',
    }, 
    #Params
    urllib.urlencode({
	    'maxCandidates': '1',
    }),
    'https://westus.api.cognitive.microsoft.com/vision/v1.0/describe')['description']['tags']
	stringToSearch = ""
	numberOfTags = len(imageTags)/3

	if (numberOfTags > 5):
		numberOfTags = 5

	for index in range(0, numberOfTags):
		stringToSearch += imageTags[index] + " "

	stringToSearch += "text only quotes"
	return stringToSearch

##Not needed because faceGenerate includes emotionGenerate
# def emotionGenerate():
# 	emotionList = processRequest(body, {}, 
# 	{#Header
# 		'Content-Type': 'application/json',
# 	    'Ocp-Apim-Subscription-Key': '4aad93e39f894f4ba3ca5fb92bede45f',
#     }, 
#     #Params
#     urllib.urlencode({
#     	'faceRectangle': None,
#     }),
#     'https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize')
# 	print (emotionList)

# def faceGenerate():
# 	faceList = processRequest(body, {}, 
# 	{#Header
# 		'Content-Type': 'application/json',
# 	    'Ocp-Apim-Subscription-Key': 'c629a44202f148d7a4b8f4540c22d4cd',
#     }, 
#     #Params
#     urllib.urlencode({
#     }),
#     'https://westus.api.cognitive.microsoft.com/face/v1.0/detect')
# 	print (faceList)

if __name__ == "__main__":
	print tagGenerate()