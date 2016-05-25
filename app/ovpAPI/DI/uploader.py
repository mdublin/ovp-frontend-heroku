import BC
import collections 

def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data


# handling ImmutableMultiDict from videoupload endpoint

def meta_parser(data):
    data = convert(data)
    title = data['videoTitle'][0]
    description = data['videoDescription'][0]
    #tags = data['videoTags'][0].splits(",")
    tags = data['videoTags'][0]
    print("meta_parser() printing: {},{},{}".format(title, description, tags))
    print(title, description, tags)
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


