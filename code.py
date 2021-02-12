import os
import uuid
import sys
import matplotlib.image as mpimg
from azure.storage.blob import BlockBlobService, PublicAccess
import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
# To install this module, run:
# python -m pip install Pillow
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person

# ----------------------------------------------------------------------------------------------------------


def run_sample():
    try:
        # Create the BlockBlobService that is used to call the Blob service for the storage account
        blob_service_client = BlockBlobService(
            account_name='', account_key='')  # provide your blob credentials

        # Create a container called 'quickstartblobs'.
        container_name = 'dummyimages'
        blob_service_client.create_container(container_name)

        # Set the permission so the blobs are public.
        blob_service_client.set_container_acl(
            container_name, public_access=PublicAccess.Container)
        # List the blobs in the container
        print("\nList blobs in the container")
        generator = blob_service_client.list_blobs(container_name)
        #condition to check with the image based on Uid
        for blob in generator:
            print(blob.name)
    except Exception as e:
        print(e)



# Main method.
if __name__ == '__main__':

    run_sample()
    # This key will serve all examples in this document.
    KEY = ""  #face api credentials (can be obtained from the azure portal)

# This endpoint will be used in all examples in this quickstart.
    ENDPOINT = "" 
    face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

    blobImage = 'abc.jpeg'
    blobUrl = "https://skfacialsystem.blob.core.windows.net/dummyimages/";
    response = requests.get(blobUrl+blobImage)

    image_bytes = io.BytesIO(response.content) 
    img =Image.open(image_bytes)
 
    inputImagedata = open('xyz.jpeg', 'rb') #input image (can be from a web ui or any storage device)
    
    

# We use detection model 3 to get better performance.

    detected_faces1 = face_client.face.detect_with_url(blobUrl+blobImage, detection_model='detection_03')
    blobImageId = detected_faces1[0].face_id

    detected_faces = face_client.face.detect_with_stream(data, detection_model='detection_03')
    inputImageId=detected_faces[0].face_id

    verify_result_same = face_client.face.verify_face_to_face(blobImageId, inputImageId)
    print(verify_result_same.confidence)
