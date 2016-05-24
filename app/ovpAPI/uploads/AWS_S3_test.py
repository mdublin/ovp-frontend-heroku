import boto3
import botocore

s3 = boto3.resource('s3')

s3_bucket_name = 'dublindev'

def AWSConnector(videofile):

    for bucket in s3.buckets.all():
        bucket = bucket
        print(bucket.name)
    

    try: 
        s3.meta.client.head_bucket(Bucket='dublindev')
        video_file = open('MyStream_2.mp4', 'rb')
        s3.Bucket('dublindev').put_object(Key='MyStream_2.mp4', Body=video_file)
        for bucket in s3.buckets.all():
            for key in bucket.objects.all():
                #print(key.key)
                if key.key == 'MyStream_2.mp4':
                    print(True)
                    print(key.key)
                    key_name = key.key
                    #url = '{}/{}/{}'.format(s3.meta.endpoint_url, bucket, key)
                    #print(url)
                    bucket_location = boto3.client('s3').get_bucket_location(Bucket=s3_bucket_name)
                    object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(bucket_location['LocationConstraint'], s3_bucket_name, key_name)
                    print(object_url)

    except botocore.exceptions.ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            exists = False

video = "foo"
test = AWSConnector(video)

