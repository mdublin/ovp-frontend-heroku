

def input_prep(user_tag):
    '''
    This provides some amount of tolerance for user input of multiple tags with formatting for URL encoding, etc. We have very explicit instructions on form for the user, although this could be improved...
    For example, if user submits: 
        sports,basketball,nba, SMGV 
    You wind up with:
        [u'sports', u'basketball', u'nba', u'%20SMGV']
        which then becomes, via the video_feed_parser script:
            &any=tag:sports&any=tag:basketball&any=tag:nba&any=tag:%20SMGV 
        So then the Brightcove CMS is being search for the tag " SMGV" instead of just "SMGV"

    '''

    print("THIS IS user_tag in input_prep")
    print(user_tag)

    #hopefully user submitted tags properly
    #contains cleaned up tags
    tags_package = []
   
    # checking if there are commas in user_tag (which should mean that the user has submitted multiple, comma-separated, tags
    if ',' in user_tag:
        #break up the comma separated tags into a list
        tags = user_tag.split(',')

        #refactoring our tags list with a list comprehension to elminate leading whitespace in front of tag words
        tags = [word.lstrip() for word in tags]

        #check if each tag element in the list has any spaces, like 'United States', and replace that space with the URL encoded version of %20
        for tag in tags:
            if ' ' in tag:
                tag = tag.replace(" ", "%20")
                tags_package.append(tag)
            else:
                tags_package.append(tag)
                print(tags_package)

        return tags_package

    #checking if single tag has spaces, like "United States"
    elif " " in user_tag:
        #format single tag with spaces for URL
        tag = str(user_tag.replace(" ", "%20"))
        return tag
    #single tag
    else:
        print "else"
        tag = str(user_tag)
        return tag







