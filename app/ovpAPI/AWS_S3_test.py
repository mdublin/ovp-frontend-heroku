import boto3
import botocore
import os

s3 = boto3.resource('s3')

s3_bucket_name = 'dublindev'

def AWSConnector(videofile_name):
    videofile_path = "./app/ovpAPI/uploads/" + videofile_name

    for bucket in s3.buckets.all():
        bucket = bucket
        print(bucket.name)
    try: 
        s3.meta.client.head_bucket(Bucket='dublindev')
        #video_file = open('MyStream_2.mp4', 'rb')
        video_file = open(videofile_path, 'rb')
        #s3.Bucket('dublindev').put_object(Key='MyStream_2.mp4', Body=video_file)
        
        s3.Bucket('dublindev').put_object(Key=videofile_name, Body=video_file)
        for bucket in s3.buckets.all():
            for key in bucket.objects.all():
                #print(key.key)
                if key.key == videofile_name:
                    print(key.key)
                    key_name = key.key
                    bucket_location = boto3.client('s3').get_bucket_location(Bucket=s3_bucket_name)
                    object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(bucket_location['LocationConstraint'], s3_bucket_name, key_name)

    except botocore.exceptions.ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            exists = False

    return object_url


