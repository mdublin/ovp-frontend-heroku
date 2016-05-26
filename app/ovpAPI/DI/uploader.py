import BC
import collections 

# converts encoding of dictionary we created from ImmutableMultiDict sent via AJAX on videoupload page
def convert(data):
    '''
    http://stackoverflow.com/questions/1254454/fastest-way-to-convert-a-dicts-keys-values-from-unicode-to-str
    '''
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



def BCDI(video_asset_url, video_meta_data):
    '''
    sends video metadata from
    videoupload form and video url from AWS S3 
    to Brightcove Dynamic Ingest
    '''
    data = convert(video_meta_data)
    name = data['videoTitle'][0]
    desc = data['videoDescription'][0]
    #tags = data['videoTags'][0].splits(",")
    tags = data['videoTags'][0]
    tags = tags.split(",")
    tags = filter(None, tags)
    url = video_asset_url

    #dedupe check for uploading
    if not BC.videoNameExists(name):
        print("did not see video, submitting to OVP CMS...")
        print(name, url, tags, desc)
        print(type(name), type(url), type(tags), type(desc))
        create_video = BC.createAndIngest(name, url, tags, desc)
        print("after create_video")

    else:
        print "video was found in OVP CMS.."





#tags = tags.split(",")
#clean up
#tags = filter(None, tags)

