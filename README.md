To start gunicorn server locally you need to swap out the configuration in wsgi.py to "production" instead of "production_heroku".

Then run: 
$ gunicorn app.wsgi:application --log-level debug

(Leaving run.py file in case you want to use Flask server instead of Gunicorn)

For Heroku deployment, just make sure the wsgi.py is pointing to "production_heroku"

Some userful Heroku commands:

    Logging:

    heroku logs --tail

    Access the shell of your one-off dyno:

    heroku run bash

Also, if you want to work on the same repository that is for the same Heroku app, you need to connect the repository copies on your other machines to the same app via: 

$ heroku git:remote -a yourappname

The other way to get the actual repository that's used for the app is to git clone it from the Heroku dashboard, but that won't actually be connected to your github repository version unless you create a new github repository, push it, etc. 



For local dev, sometimes port gets stuck -- to find offending port:
    $ lsof -n -i4TCP:8000 | grep LISTEN




AWS S3:
 
Basically we're using a public-access bucket on AWS S3 to upload video assets and be able generate/grab publically available file URLs so that they can be passed to Brightcove's Dynamic Ingest API (although this is useful for any other OVP with a similar ingest option). 

To configure your S3 bucket, here's an easy way that works as of this writing: 

1. Sign into Amazon Web Services and go to S3 Management Console

2. Click the Properties button for the desired bucket

3. Go to Permissions tab and hit Add Bucket Policy link (or Edit Bucket Policy if you've already added one previously). 

4. Copy and paste the following into the Bucket Policy Editor popup. Replace "YOUR-BUCKET-NAME" with your own bucket's name: 

{"Version": "2008-10-17",
"Statement": [{"Sid": "AllowPublicRead",
"Effect": "Allow",
"Principal": {
"AWS": "*"
},
"Action": "s3:GetObject",
"Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/*"
}]}

It doesn't seem like this should work, and you should use the Policy Generator ( http://awspolicygen.s3.amazonaws.com/policygen.html ), but the above really does work. 


