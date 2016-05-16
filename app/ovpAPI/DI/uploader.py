import BC


# file handling

name = ""
desc = ""
url = ""

tags = user_submitted_tags.split(",")
#clean up
tags = filter(None, tags)



#dedupe check for uploading
if not BC.videoNameExists(name):
    print("did not see video, submitting to OVP CMS...")
    
    create_video = BC.createAndIngest(name, url, tags, desc)
    
else:
    print "video was found in OVP CMS.."


