import httplib, urllib, base64
import os, requests, cv2, base64

from helper import processRequest

def generate_tags(photoUrl):
    imageTags = processRequest(
        'https://westus.api.cognitive.microsoft.com/vision/v1.0/describe',
        {"url": photoUrl},
        {}, 
        {#Header
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': '72608f3be7934eaeb9ea0ecf60e585da',
        },
        #Params
        urllib.urlencode({
            'maxCandidates': '1',
        })
    )
    imageTags = imageTags['description']['tags']
    stringToSearch = ""
    numberOfTags = len(imageTags)/3

    if (numberOfTags > 5):
        numberOfTags = 5

    for index in range(0, numberOfTags):
        stringToSearch += imageTags[index] + " "

    # stringToSearch += "text only quotes"
    return stringToSearch

##Not needed because faceGenerate includes emotionGenerate
# def emotionGenerate():
#   emotionList = processRequest(body, {}, 
#   {#Header
#       'Content-Type': 'application/json',
#       'Ocp-Apim-Subscription-Key': '4aad93e39f894f4ba3ca5fb92bede45f',
#     }, 
#     #Params
#     urllib.urlencode({
#       'faceRectangle': None,
#     }),
#     'https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize')
#   print (emotionList)

# def faceGenerate():
#   faceList = processRequest(body, {}, 
#   {#Header
#       'Content-Type': 'application/json',
#       'Ocp-Apim-Subscription-Key': 'c629a44202f148d7a4b8f4540c22d4cd',
#     }, 
#     #Params
#     urllib.urlencode({
#     }),
#     'https://westus.api.cognitive.microsoft.com/face/v1.0/detect')
#   print (faceList)

if __name__ == "__main__":
    print tagGenerate()