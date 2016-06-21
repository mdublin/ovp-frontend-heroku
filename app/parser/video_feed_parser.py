#! /usr/bin/python
# -*- coding: utf-8 -*-

print "Content-type: application/json\n\n"
import feedparser


# receiving user_tag text submitted by user via TagSearchForm on
# http://127.0.0.1:5000/protected
def load(parser_input, page, results_per_page):

    # checking parser_input object type
    if isinstance(parser_input, str):
        video_feed = 'http://api.brightcove.com/services/library?command=search_videos&any=tag:{}&output=mrss&media_delivery=http&sort_by=CREATION_DATE:DESC&token=8-XmRYT4C6VKYvvCGoJhcaGFX-t7ZO-ML3eXD95oalq6obm5ho7eJg..'.format(
            parser_input)

    # for multiple tags
    else:
        tags_insert = ""
        for tag in parser_input:
            urlencode = "&any=tag:" + tag
            tags_insert += urlencode

        video_feed = 'http://api.brightcove.com/services/library?command=search_videos{}&output=mrss&media_delivery=http&sort_by=CREATION_DATE:DESC&token=8-XmRYT4C6VKYvvCGoJhcaGFX-t7ZO-ML3eXD95oalq6obm5ho7eJg..'.format(
            tags_insert)

    d = feedparser.parse(video_feed)

    response_array = []

    # list returned of dicts for each video, this will be sent to, and
    # iterated through, videofeed.html endpoint with jinja2 control structures
    asset_return_list = []

    # -- For each item in the feed
    # The value of ====> (page - 1) * results_per_page  == Start point in feed
    # The value of ====>  page * results_per_page + results_per_page == Stop point in feed
    #
    for index, post in enumerate(
            d.entries[
            (page - 1) * results_per_page:page * results_per_page + results_per_page]):
        if index >= 100:
            break
        # Here we set up a dictionary in order to extract selected data from the
        # original brightcove "post" result
        item = {}

        item['name'] = post.title,
        item['description'] = post.description,
        item['url'] = u"%s" % post.link,
        # item['tags'] = post.media_keywords.split(",")
        item['videoID'] = post.bc_titleid,

        max_bitrate = 0
        vid_url = None

        # get thumbnail image URL 
        thumbnails = post.media_thumbnail[0]
        thumbnail_url = thumbnails['url']



        videos = post.media_content
        tags = post.media_keywords

        # -- For each video in the item dict
        for video in videos:
            # -- If the video has a value for its bitrate
            if 'bitrate' in video:
                # -- Extract the value of this video's bitrate
                bitrate_str = video['bitrate']
        # -- and convert it to an integer (by default it is a string in the XML)
                curr_bitrate = int(bitrate_str)
            # -- If the bitrate of this video is greater than
            # -- the highest bitrate we've seen, mark this video as the one with
            # -- the highest birate.
                if curr_bitrate > max_bitrate:
                    max_bitrate = curr_bitrate
                vid_url = video['url']
        # -- This line simply prints out the maximum bitrate and current video URL for each iteration
        # print "{} url {}".format(max_bitrate, vid_url)
        # print "highest bitrate {} url {}".format(max_bitrate, vid_url)

        item['tags'] = tags
        item['url'] = vid_url
        item['thumbnail'] = thumbnail_url
        videoID = item['videoID']
        videoName = item['name']
        response_array.append(item)

        videoID = str(videoID)
        videoUrl = vid_url
        # videoName = str(videoName) #we have to convert videoName to a plain
        # old string instead of leaving it as unicode because the dudupe
        # function in our db script is "seeing" the video titles in our db
        for i in videoName:
            videoNameConverted = i  # Extracting the video title out of the tuple its in, so we can get string utf-8 encoded. So everwhere below this, we're replacing videoName with videoNameConverted
        # foo = type(i)
        # print "this is type check of tuple extract on line 70: %s" % foo
        videoDescription = item['description']

    #video_package = {}
    for asset_dict in response_array:
        video_package = {}
        extract_sourcefile_tupe = asset_dict['url']
        extract_videoID_tupe = asset_dict['videoID']
        extract_thumbnail_tupe = asset_dict['thumbnail']        
        extract_name_tupe = asset_dict['name']
        extract_description_tupe = asset_dict['description']
        extract_tags_tupe = asset_dict['tags']

        video_package.update(
            {
                'videoID': extract_videoID_tupe[0],
                'name': extract_name_tupe[0],
                'description': extract_description_tupe[0],
                'tags': extract_tags_tupe,
                'url': extract_sourcefile_tupe,
            'thumbnail': extract_thumbnail_tupe})
        asset_return_list.append(video_package)

    # send results to db
   # SearchResult.store(asset_return_list)

    return asset_return_list



# load all/newest media from feed

def mediaload(page, results_per_page):

    video_feed = "http://api.brightcove.com/services/library?command=search_videos&output=mrss&media_delivery=http&sort_by=CREATION_DATE:DESC&token=8-XmRYT4C6VKYvvCGoJhcaGFX-t7ZO-ML3eXD95oalq6obm5ho7eJg.."

    d = feedparser.parse(video_feed)

    response_array = []

    # list returned of dicts for each video, this will be sent to, and
    # iterated through, videofeed.html endpoint with jinja2 control structures
    asset_return_list = []

    # -- For each item in the feed
    # The value of ====> (page - 1) * results_per_page  == Start point in feed
    # The value of ====>  page * results_per_page + results_per_page == Stop point in feed
    #
    for index, post in enumerate(
            d.entries[
            (page - 1) * results_per_page:page * results_per_page + results_per_page]):
        #print index, post

        if index >= 100:
            break
        # Here we set up a dictionary in order to extract selected data from the
        # original brightcove "post" result
        item = {}

        item['name'] = post.title,
        item['description'] = post.description,
        item['url'] = u"%s" % post.link,
        # item['tags'] = post.media_keywords.split(",")
        item['videoID'] = post.bc_titleid,

        max_bitrate = 0
        vid_url = None
        videos = post.media_content

        # get thumbnail image URL 
        
        try:
            thumbnails = post.media_thumbnail[0]
            thumbnail_url = thumbnails['url']
        except AttributeError:
            thumbnail_url = None
        
        #print thumbnails
        #thumbnail_url = None
        #max_height = 90
        
        #for thumbnail in thumbnails:
        #    if 'height' in thumbnail:
        #        height = thumbnail['height']
        #        if height == '90':
        #            thumbnail_url = thumbnail['url']

        tags = post.media_keywords

        # -- For each video in the item dict
        for video in videos:
            # -- If the video has a value for its bitrate
            if 'bitrate' in video:
                # -- Extract the value of this video's bitrate
                bitrate_str = video['bitrate']
        # -- and convert it to an integer (by default it is a string in the XML)
                curr_bitrate = int(bitrate_str)
            # -- If the bitrate of this video is greater than
            # -- the highest bitrate we've seen, mark this video as the one with
            # -- the highest birate.
                if curr_bitrate > max_bitrate:
                    max_bitrate = curr_bitrate
                vid_url = video['url']
        # -- This line simply prints out the maximum bitrate and current video URL for each iteration
        # print "{} url {}".format(max_bitrate, vid_url)
        # print "highest bitrate {} url {}".format(max_bitrate, vid_url)


        item['tags'] = tags
        item['url'] = vid_url
        item['thumbnail'] = thumbnail_url

        videoID = item['videoID']
        # new line
        videoName = item['name']
        response_array.append(item)

        videoID = str(videoID)
        videoUrl = vid_url
        # videoName = str(videoName) #we have to convert videoName to a plain
        # old string instead of leaving it as unicode because the dudupe
        # function in our db script is "seeing" the video titles in our db
        for i in videoName:
            videoNameConverted = i  # Extracting the video title out of the tuple its in, so we can get string utf-8 encoded. So everwhere below this, we're replacing videoName with videoNameConverted
        # foo = type(i)
        # print "this is type check of tuple extract on line 70: %s" % foo
        videoDescription = item['description']
        
    #video_package = {}
    for asset_dict in response_array:
        video_package = {}
        extract_sourcefile_tupe = asset_dict['url']
        extract_thumbnail_tupe = asset_dict['thumbnail']
        extract_videoID_tupe = asset_dict['videoID']
        extract_name_tupe = asset_dict['name']
        extract_description_tupe = asset_dict['description']
        extract_tags_tupe = asset_dict['tags']

        video_package.update(
            {
                'videoID': extract_videoID_tupe[0],
                'name': extract_name_tupe[0],
                'description': extract_description_tupe[0],
                'tags': extract_tags_tupe,
                'url': extract_sourcefile_tupe,
                'thumbnail': extract_thumbnail_tupe
            }
        )
        
        asset_return_list.append(video_package)

    # send results to db
    # SearchResult.store(asset_return_list)

    return asset_return_list 
