import boto3

s3 = boto3.resource('s3')

for bucket in s3.buckets.all():
    print(bucket.name)
    

try: 
    s3.meta.client.head_bucket(Bucket='dublindev')
    video_file = open('image.mp4', 'rb')
    s3.Bucket('dublindev').put_object(Key='image.mp4', Body=video_file)
    for bucket in s3.buckets.all():
        for key in bucket.objects.all():
            print(key.key)
except botocore.exceptions.ClientError as e:
    error_code = int(e.response['Error']['Code'])
    if error_code == 404:
        exists = False

