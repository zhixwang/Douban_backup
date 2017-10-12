"""

@author: zxwang zxwang.pku@gmail.com
"""
import re
import urllib2
import urllib
from bs4 import BeautifulSoup
import codecs
import config as config


def get_url_content(url):   # fetch the webpage
    i_headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",\
                 "Referer": 'http://www.baidu.com'}
    req = urllib2.Request(url, headers=i_headers)
    return urllib2.urlopen(req).read()

def change_line(out_file,file_name):    # output a '\n' character
    out_file.close()
    out_file=open(file_name,'a')
    out_file.write('\n')
    out_file.close()
    out_file = codecs.open(file_name,'a','utf-8')
    return out_file

# write output files
def output_data(file_name,total_num,title_list,comment_list,rating_list):
    try:
        out_file = codecs.open(file_name,'a','utf-8')
    except:
        print "Output file open failed!"
    else:
        pass
    for i in range(0,total_num):
        out_file.write(title_list[i])
        if rating_list[i]:
            out_file.write(u': Rate: ')
            out_file.write(rating_list[i])
        out_file = change_line(out_file,file_name)
        if comment_list[i]:
            out_file.write(u'Comment: ')
            out_file.write(comment_list[i])
            out_file = change_line(out_file,file_name)
        out_file = change_line(out_file,file_name)   
    out_file.close()

def grab_book(user_id):     #grab book information, because book has different titling method
    file_name='book.txt'
    file_link = u'https://book'+u'.douban.com/people/'+user_id+u'/collect'
    fetch_url = file_link
    content = get_url_content(fetch_url)
    soup = BeautifulSoup(content)
    total_num = int(re.findall('[0-9]+',soup.title.prettify())[0]) # The books that have read
    pages = total_num/15+1  # number of pages
    title_list = []
    comment_list = []
    rating_list = []
    for page_id in range(0,pages):
        start_id = 15*page_id
        fetch_url=file_link+u'?start='+str(start_id)+u'&sort=time&rating=all&filter=all&mode=grid'
        try:
            content = get_url_content(fetch_url)
        except:
            print "Download webpage failed"
            break
        else:
            print "Page "+str(page_id+1)+" Downloaded:"
        soup = BeautifulSoup(content)
        if page_id == pages-1:                  # numbers of item in this page
            item_limit = total_num-page_id*15
        else:
            item_limit = 15  
        count = 0
        
        tmp_title_list=[]
        for link in soup.find_all('a'):
            if count > item_limit-1 :
                break
            if link.get('title'):
                print "Item:"+link.get('title')
                title_list.append(link.get('title'))
                tmp_title_list.append(link.get('title'))
            else:
                continue
            # get comments
            raw_comment = soup.select('p[class^="comment"]')[count] # original information containing comment
            comment =  re.findall("comment\">\n\s(.*)\n</p>",raw_comment.prettify())
            count = count +1
            if len(comment) > 0:
                comment = comment[0]
                print "comment:"+comment
            comment_list.append(comment)
        #deal with rating
        ratings = [None]*item_limit
        raw_ratings = soup.select('span[class^="rating"]')
        n_rat = len(raw_ratings)    # number of ratings
        for i in range(0,n_rat):
            rate_title = raw_ratings[i].find_previous('a').get('title')
            raw_rating = soup.select('span[class^="rating"]')[i].prettify()
            rating = re.findall('[1-5]',raw_rating)[0]
            if rate_title in tmp_title_list:
                idx = tmp_title_list.index(rate_title)
                ratings[idx] = rating
        rating_list.extend(ratings)
    output_data(file_name,total_num,title_list,comment_list,rating_list)
        
def grab_data(kind,user_id):
    if kind == 'book':
        file_name='book.txt'
        file_link = u'https://book'+u'.douban.com/people/'+user_id+u'/collect'
    elif kind == 'movie':
        file_name='movie.txt'
        file_link = u'https://movie'+u'.douban.com/people/'+user_id+u'/collect'
    elif kind == 'music':
        file_name='music.txt'
        file_link = u'https://music'+u'.douban.com/people/'+user_id+u'/collect'
    else:
        print "Unknown kind!"
        return
    
    fetch_url = file_link
    content = get_url_content(fetch_url)
    soup = BeautifulSoup(content)
    total_num = int(re.findall('[0-9]+',soup.title.prettify())[0]) # The books that have read
    pages = total_num/15+1  # number of pages
    title_list = []
    comment_list = []
    rating_list = []
    for page_id in range(0,pages):
        start_id = 15*page_id
        fetch_url=file_link+u'?start='+str(start_id)+u'&sort=time&rating=all&filter=all&mode=grid'
        try:
            content = get_url_content(fetch_url)
        except:
            print "Download webpage failed"
            break
        else:
            print "Page "+str(page_id+1)+" Downloaded:"
        soup = BeautifulSoup(content)
        if page_id == pages-1:                  
            item_limit = total_num-page_id*15
        else:
            item_limit = 15
        tmp_title_list=[]
        raw_titles = soup.select('em')
        t_num = len(raw_titles)
        for item_id in range(0,t_num):
            item_title = re.findall("em>\n\s(.*)\n</em>",raw_titles[item_id].prettify())[0]
            tmp_title_list.append(item_title)
            title_list.append(item_title)
            print item_title
        # get comments
        comments = [None]*item_limit
        raw_comments = soup.select('span[class^="comment"]')
        n_com = len(raw_comments)    # number of ratings
        for i in range(0,n_com):
            raw_com_title = raw_comments[i].find_previous('em') # look for the title of the comment
            com_title = re.findall("em>\n\s(.*)\n</em>",raw_com_title.prettify())[0]
            comment = re.findall("comment\">\n\s(.*)\n</span>",raw_comments[i].prettify())[0]
            if com_title in tmp_title_list:
                idx = tmp_title_list.index(com_title)
                comments[idx] = comment
        comment_list.extend(comments)    
        #deal with rating
        ratings = [None]*item_limit
        raw_ratings = soup.select('span[class^="rating"]')
        n_rat = len(raw_ratings)    # number of ratings
        for i in range(0,n_rat):
            raw_rate_title = raw_ratings[i].find_previous('em')
            rate_title = re.findall("em>\n\s(.*)\n</em>",raw_rate_title.prettify())[0]
            raw_rating = soup.select('span[class^="rating"]')[i].prettify()
            rating = re.findall('[1-5]',raw_rating)[0]
            if rate_title in tmp_title_list:
                idx = tmp_title_list.index(rate_title)
                ratings[idx] = rating
        rating_list.extend(ratings)
    output_data(file_name,total_num,title_list,comment_list,rating_list)


user = config.User_id
if config.Book == True:
    grab_book(user)
if config.Movie == True:
    grab_data('movie',user)
if config.Music == True:
    grab_data('music',user)

    


    

