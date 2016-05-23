import BC

# handling ImmutableMultiDict from videoupload endpoint

def meta_parser(data):
    
    title = data['video_title'][0]
    description = data['video_description'][0]
    tags = data['video_tags'][0]
    print("meta_parser() printing: {},{},{}".format(title, description, tags))
    return (title, description, tags)


# file handling

name = ""
desc = ""
url = ""
tags = ""

tags = tags.split(",")
#clean up
tags = filter(None, tags)



#dedupe check for uploading
#if not BC.videoNameExists(name):
#    print("did not see video, submitting to OVP CMS...")
    
#    create_video = BC.createAndIngest(name, url, tags, desc)
    
#else:
#    print "video was found in OVP CMS.."


