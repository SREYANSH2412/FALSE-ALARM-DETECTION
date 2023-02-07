import boto3
import io
import csv
from http import client
from PIL import Image, ImageDraw, ExifTags, ImageColor, ImageFont
# from pygame import mixer
import time


with open('cred.csv','r') as input:
    next(input)
    reader = csv.reader(input)
    for line in reader:
        access_key_id=line[2]
        secret_access_key=line[3]

client=boto3.client('rekognition',
                        region_name='ap-south-1', 
                        aws_access_key_id=access_key_id,
                        aws_secret_access_key=secret_access_key)
    
    
response=client.compare_faces(
    SourceImage={
        'S3Object':{
            'Bucket':'sih-face-recognition',
            'Name':'IMG_20220826_140416.jpg'
        }
    },
    TargetImage={
        'S3Object':{
            'Bucket':'sih-face-recognition',
            'Name': 'IMG_20220826_153728.jpg'
        }
    },
)
    
for key, value in response.items():
    if key in ('FaceMatches', 'UnmatchedFaces'):
        print(key)
        res1=[]
        for i in range (len(value)):
            if key in ('FaceMatches'):
                res1.append(value[i].get('Similarity'))
        print(res1)


# if(len(res1)==0):
#     print('no faces matched')
# elif(len(res1)==1):
#     for i in range (len(res1)):
#         if(res1[i]>80.0):
#             print("person recognised")
#         else:
#             print("person not recognised")
        #         print('Similarity = ',len(res1))
        #     elif key in ('UnmatchedFaces'):
        #         res1.append(value[i].get('Similarity'))
        #         print('Dissimilarity = ',len(res1))
        # for att in value:
        #         print(att)

# print("Face matched")
# print("Access granted")
