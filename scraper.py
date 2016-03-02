#!/usr/bin/env python

import scraperwiki
import requests
import lxml.html
import re
#https://www.instagram.com/explore/tags/%E2%9C%A8/

#Copy and paste a column from excel within the ''' markers to create a variable
pastedfromexcel = '''one
two'''

#This then splits that variable on each carriage return, to create a list of usernames
taglist = pastedfromexcel.split('\n')
taglist = ['xmasjumperday', 'christmasjumperday']
baseurl = 'https://www.instagram.com/explore/tags/'

#Here we define a function which uses the username as an argument
def grabfollows(tagurl, nextpage, pages):
    #create the full URL by joining the username to the baseurl
    userurl = tagurl+nextpage
    print "SCRAPING", userurl
    pages = pages+1
    print "PAGE", pages
    if pages < 100:
        #scrape it into 'html'
        #THIS GENERATES AN ERROR IF THE URL HAS DISAPPEARED
        html = scraperwiki.scrape(userurl)
        #convert it to an lxml object
        root = lxml.html.fromstring(html)
        print root
        #grab meta tag with name attribute as specified
        meta = root.cssselect('meta[name="description"]')
        #grab content= value
        print "META", meta[0].attrib.get('content')
        description = meta[0].attrib.get('content')
        #grab anything in <script> tags
        headers = root.cssselect('script')
        #the 7th one (index 6) has what we need
        profiledata = headers[6].text
        #split the contents of that tag in three, grab the second part (after the first mention of nodes)
        recentposts = profiledata.split('"nodes":')[1]
        print "nodes", len(recentposts)
        pics = recentposts.split('"code":"')
        print "pics", len(pics)
        idlist = []
        for pic in pics[1:-1]:
            print "PIC", pic
            picurlid = pic.split('"')[0]
            print picurlid
            ownerid = pic.split('"owner":{"id":"')[1].split('"}')[0]
            if len(pic.split('"owner":{"id":"'))>1:
                comments = pic.split('comments":{"count":')[1].split('}')[0]
            else:
                comments = "NO COMMENTS"
            if len(pic.split('caption":'))>1:
                caption = pic.split('caption":')[1].split('}')[0]
                if len(caption.split('likes":'))>1:
                    likes = caption.split('likes":')[1].split('}')[0].replace('{"count":','')
                else:
                    likes = "NULL"
            else:
                caption = "NO CAPTION"
                likes = pic.split('likes":')[1].split('}')[0].replace('{"count":','')
            date = pic.split('date":')[1].split(',')[0]
            isvideo = pic.split('is_video":')[1].split(',')[0]
            photoid = pic.split('id":"')[2].split('",')[0]
            print "PHOTOID", photoid
            idlist.append(photoid)
            print ownerid, comments, caption, likes, date, isvideo
            #create the fields in our dictionary, and assign variables to those
            record['ownerid'] = ownerid
            record['photoid'] = photoid
            record['comments'] = comments
            record['likes'] = likes
            record['caption'] = caption
            record['date'] = date
            record['isvideo'] = isvideo
            record['picurlid'] = picurlid
            record['description'] = description
            record['userurl'] = userurl
            print record
            #save the whole thing, with username as the unique key
            scraperwiki.sql.save(['picurlid'], record, table_name='xmasjumper')
        print "HAHAHA 1140637147849465299"
        #print photoid
        print max(idlist)
        print min(idlist)
        nextpage = '/?max_id='+min(idlist)
        print nextpage
        grabfollows(tagurl, nextpage, pages)

#create an empty record (this will be filled when the function runs above)
record = {}
pages = 0
#this needs to start from '' to work properly. Otherwise you impose one city's max_id on another
nextpage = ''

#loop through our username list
for tag in taglist: # the list of [leeds, manchester]
    #run the function defined above on each username
    tagurl = baseurl+tag
    grabfollows(tagurl, nextpage, pages)

#grabfollows('https://www.instagram.com/explore/tags/', nextpage, pages)
