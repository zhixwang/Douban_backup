"""

@author: zxwang zxwang.pku@gmail.com
@contributor: Michael Shih michael_shi@live.com
"""
import re
#import urllib2
import urllib
import urllib.request
from bs4 import BeautifulSoup
import codecs
import config as config
import xlwt
import pandas as pd

def get_url_content(url):   # fetch the webpage
    i_headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",\
                 "Referer": 'http://www.bing.com'}
    #req = urllib2.Request(url, headers=i_headers)
    req = urllib.request.Request(url, headers=i_headers)
    #return urllib2.urlopen(req).read()
    return urllib.request.urlopen(req).read()

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
        print ("Output file open failed!")
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

def output_more_data(file_name,total_num,title_list,comment_list,rating_list, date_list):
    try:
        out_file = codecs.open(file_name,'a','utf-8')
    except:
        print ("Output file open failed!")
    else:
        pass
    for i in range(0,total_num):
        out_file.write(title_list[i])
        if rating_list[i]:
            out_file.write(u': Rate: ')
            out_file.write(rating_list[i])
        #out_file = change_line(out_file,file_name)
        if date_list[i]:
            out_file.write(u' Date: ')
            out_file.write(date_list[i])
        out_file = change_line(out_file, file_name)
        if comment_list[i]:
            out_file.write(u' Comment: ')
            out_file.write(comment_list[i])
            out_file = change_line(out_file,file_name)
        out_file = change_line(out_file,file_name)   
        
    out_file.close()

#set sheet style 
def set_sheetstyle(name,height,bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    style.alignment.wrap = 1 #auto wrap
    return style

# write Excel document
def write_book_excel(total_num,title_list,comment_list,rating_list, date_list, author_list, price_list, pub_list, releasedate_list):
    output_dict = {'Title': title_list, "Rate": rating_list, "Author": author_list, \
                   "Release Date": releasedate_list, "Price": price_list, "Pub" : pub_list, \
                  "Comment": comment_list}    
    output_df = pd.DataFrame(output_dict)    
    output_df.to_excel("collectBook.xlsx")
    
    # workbook = xlwt.Workbook()
    # sheet1 = workbook.add_sheet('Books',cell_overwrite_ok=True)
    # rowTitle = ["Title","Rate","Date","Author","Release Date","Price","Pub","Comment"]
    # #colum0 = ["col1","col2","col3","col4","col5","col6"]
    # #
    # sheet1.col(0).width = 256 * 20
    # sheet1.col(1).width = 256 * 4
    # sheet1.col(2).width = 256 * 15 #date
    # sheet1.col(3).width = 256 * 20 #author
    # sheet1.col(4).width = 256 * 15 #release date
    # sheet1.col(5).width = 256 * 10  #price
    # sheet1.col(6).width = 256 * 25 #pub
    # sheet1.col(7).width = 256 * 100 #comment

    # for i in range(0,len(rowTitle)):
    #     sheet1.write(0,i,rowTitle[i],set_sheetstyle('Microsoft YaHei',220,True))

    # for i in range(0,total_num):
    #     sheet1.write(i+1,0,title_list[i],set_sheetstyle('Microsoft YaHei',220,False))
    #     if rating_list[i]:
    #         sheet1.write(i+1,1,rating_list[i],set_sheetstyle('Microsoft YaHei',220,False))
    #     if date_list[i]:
    #         sheet1.write(i+1,2,date_list[i],set_sheetstyle('Microsoft YaHei',220,False))
    #     if author_list[i]:
    #         sheet1.write(i+1,3,author_list[i],set_sheetstyle('Microsoft YaHei',220,False))
    #     if releasedate_list[i]:
    #         sheet1.write(i+1,4,releasedate_list[i],set_sheetstyle('Microsoft YaHei',220,False))
    #     if price_list[i]:
    #         sheet1.write(i+1,5,price_list[i],set_sheetstyle('Microsoft YaHei',220,False))
    #     if pub_list[i]:
    #         sheet1.write(i+1,6,pub_list[i],set_sheetstyle('Microsoft YaHei',220,False))
    #     if comment_list[i]:
    #         sheet1.write(i+1,7,comment_list[i],set_sheetstyle('Microsoft YaHei',220,False))

    # workbook.save('collectBook.xls')

def grab_book(user_id):     #grab book information, because book has different titling method
    file_name='book.txt'
    file_link = u'https://book'+u'.douban.com/people/'+user_id+u'/collect'
    fetch_url = file_link
    content = get_url_content(fetch_url)
    soup = BeautifulSoup(content)
    total_num = int(re.findall('[0-9]+',soup.title.prettify())[0]) # The books that have read
    pages = int(total_num/15+1)  # number of pages
    title_list = []
    comment_list = []
    date_list = [] # michael added @20190819
    author_list = []
    releasedate_list = []
    price_list = []
    pubs_list = [] # michael added @20190819
    rating_list = []
    for page_id in range(0,pages):
        start_id = 15*page_id
        fetch_url=file_link+u'?start='+str(start_id)+u'&sort=time&rating=all&filter=all&mode=grid'
        try:
            content = get_url_content(fetch_url)
        except:
            print ("Download webpage failed")
            break
        else:
            print ("Page "+str(page_id+1)+" Downloaded:")
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
                print ("Item:"+link.get('title'))
                title_list.append(link.get('title'))
                tmp_title_list.append(link.get('title'))
            else:
                continue
            # get comments
            raw_comment = soup.select('p[class^="comment"]')[count] # original information containing comment
            comment =  re.findall("comment\">\n\s(.*)\n</p>",raw_comment.prettify())
            # comment =  raw_comment.get_text()

             # michael modified == get dates
            raw_inputdate = soup.select('span[class^="date"]')[count]
            inputdate = re.findall(r"(\d{4}-\d{1,2}-\d{1,2})",raw_inputdate.prettify())
            # inputdate = raw_inputdate.get_text()
            
            # michael modified == get pubs
            raw_pub = soup.select('div[class^="pub"]')[count]
            pub =  re.findall("pub\">\n\s(.*)\n</div>", raw_pub.prettify())    
            # pub = raw_pub.get_text()
            
            count = count +1
            if len(comment) > 0:
                comment = comment[0]
                print ("comment:"+comment)
            comment_list.append(comment)
           
            if len(inputdate) > 0:
                inputdate = inputdate[0]
            date_list.append(inputdate)

            if len(pub) > 0:
                pub = pub[0]
                if len(pub) > 0:
                    props = pub.split('/')
                    author = props[0]
                    if len(props) == 5:
                        pub = props[2]
                        releasedate = props[3]
                        price = props[4]
                    elif len(props) == 4:
                        pub = props[1]
                        releasedate = props[2]
                        price = props[3]
                    else:
                        pub = ''
                        releasedate = ''
                        price = 0

            author_list.append(author)
            pubs_list.append(pub)
            releasedate_list.append(releasedate)
            price_list.append(price)

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

    if config.Out_Put_Type == 0:    
        output_more_data(file_name,total_num,title_list,comment_list,rating_list, date_list)
    elif config.Out_Put_Type == 1:
        pass
        write_book_excel(total_num,title_list,comment_list,rating_list, date_list, author_list, price_list, pubs_list, releasedate_list)

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
        print ("Unknown kind!")
        return
    
    fetch_url = file_link
    content = get_url_content(fetch_url)
    soup = BeautifulSoup(content)
    total_num = int(re.findall('[0-9]+',soup.title.prettify())[0]) # The books that have read
    pages = int(total_num/15+1)  # number of pages
    title_list = []
    intro_list = []
    inputdate_list = []
    comment_list = []
    rating_list = []
    for page_id in range(0,pages):
        start_id = 15*page_id
        fetch_url=file_link+u'?start='+str(start_id)+u'&sort=time&rating=all&filter=all&mode=grid'
        try:
            content = get_url_content(fetch_url)
        except:
            print( "Download webpage failed")
            break
        else:
            print ("Page "+str(page_id+1)+" Downloaded:")
        soup = BeautifulSoup(content)
        if page_id == pages-1:                  
            item_limit = total_num-page_id*15
        else:
            item_limit = 15
        tmp_title_list=[]
        raw_titles = soup.select('em')
        raw_intros = soup.select('li[class="intro"]') 
        raw_inputdates = soup.select('span[class="date"]')
        t_num = len(raw_titles)
        for item_id in range(0,t_num):
            # item_title = re.findall("em>\n\s(.*)\n</em>",raw_titles[item_id].prettify())[0]
            item_title = raw_titles[item_id].get_text() 
            # item_intro = re.findall("intro\">\n\s(.*)\n</li>", raw_intros[item_id].prettify())[0]
            item_intro = raw_intros[item_id].get_text() 
            # item_inputdates = re.findall("date\">\n\s(.*)\n</span>", raw_inputdates[item_id].prettify())[0]
            item_inputdates = raw_inputdates[item_id].get_text() 
            tmp_title_list.append(item_title)
            title_list.append(item_title)
            intro_list.append(item_intro)
            inputdate_list.append(item_inputdates)
            #print (item_title)

        # get comments
        comments = [None]*item_limit
        raw_comments = soup.select('span[class^="comment"]')
        n_com = len(raw_comments)    # number of ratings
        for i in range(0,n_com):
            raw_com_title = raw_comments[i].find_previous('em') # look for the title of the comment
            # com_title = re.findall("em>\n\s(.*)\n</em>",raw_com_title.prettify())[0]
            com_title = raw_com_title.get_text()
            # comment = re.findall("comment\">\n\s(.*)\n</span>",raw_comments[i].prettify())[0]
            comment = raw_comments[i].get_text()
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
            # rate_title = re.findall("em>\n\s(.*)\n</em>",raw_rate_title.prettify())[0]
            rate_title = raw_rate_title.get_text()
            raw_rating = soup.select('span[class^="rating"]')[i].prettify()
            rating = re.findall('[1-5]',raw_rating)[0]
            if rate_title in tmp_title_list:
                idx = tmp_title_list.index(rate_title)
                ratings[idx] = rating
        rating_list.extend(ratings)
    
    if config.Out_Put_Type == 0:  
        output_data(file_name,total_num,title_list,comment_list,rating_list)
    elif config.Out_Put_Type == 1:
        if (config.Movie == True) and (kind == 'movie'):
            write_movie_excel(total_num,title_list,comment_list,rating_list, inputdate_list, intro_list)
        if (config.Music == True) and (kind == 'music'):
            write_music_excel(total_num,title_list,comment_list,rating_list, inputdate_list, intro_list)

def write_movie_excel(total_num,title_list,comment_list,rating_list, inputdate_list, intro_list):
    output_dict = {"Title": title_list,"Rate":rating_list,"Date":inputdate_list,"Comment":comment_list,"Intro":intro_list}
    output_df = pd.DataFrame(output_dict)
    output_df.to_excel("collectMovie.xlsx")
    # workbook = xlwt.Workbook()
    # sheet1 = workbook.add_sheet('Movies',cell_overwrite_ok=True)
    # rowTitle = ["Title","Rate","Date","Comment","Intro"]
    # #
    # sheet1.col(0).width = 256 * 40
    # sheet1.col(1).width = 256 * 4
    # sheet1.col(2).width = 256 * 15 #date
    # sheet1.col(3).width = 256 * 100 #comment
    # sheet1.col(4).width = 256 * 100 #intro

    # for i in range(0,len(rowTitle)):
    #     sheet1.write(0,i,rowTitle[i],set_sheetstyle('Microsoft YaHei',220,True))

    # for i in range(0,total_num):
    #     sheet1.write(i+1,0,title_list[i],set_sheetstyle('Microsoft YaHei',220,False))
    #     if rating_list[i]:
    #         sheet1.write(i+1,1,rating_list[i],set_sheetstyle('Microsoft YaHei',220,False))
    #     if inputdate_list[i]:
    #         sheet1.write(i+1,2,inputdate_list[i],set_sheetstyle('Microsoft YaHei',220,False))
    #     if comment_list[i]:
    #         sheet1.write(i+1,3,comment_list[i],set_sheetstyle('Microsoft YaHei',220,False))
    #     if intro_list[i]:
    #         sheet1.write(i+1,4,intro_list[i],set_sheetstyle('Microsoft YaHei',220,False))
        
    # workbook.save('collectMovie.xls')

def write_music_excel(total_num,title_list,comment_list,rating_list, inputdate_list, intro_list):
    output_dict = {"Title": title_list,"Rate":rating_list,"Date":inputdate_list,"Comment":comment_list,"Intro":intro_list}
    output_df = pd.DataFrame(output_dict)
    output_df.to_excel("collectMusic.xlsx")
    # workbook = xlwt.Workbook()
    # sheet1 = workbook.add_sheet('Movies',cell_overwrite_ok=True)
    # rowTitle = ["Title","Rate","Date","Comment","Intro"]
    # #
    # sheet1.col(0).width = 256 * 40
    # sheet1.col(1).width = 256 * 4
    # sheet1.col(2).width = 256 * 15 #date
    # sheet1.col(3).width = 256 * 100 #comment
    # sheet1.col(4).width = 256 * 100 #intro

    # for i in range(0,len(rowTitle)):
    #     sheet1.write(0,i,rowTitle[i],set_sheetstyle('Microsoft YaHei',220,True))

    # for i in range(0,total_num):
    #     sheet1.write(i+1,0,title_list[i],set_sheetstyle('Microsoft YaHei',220,False))
    #     if rating_list[i]:
    #         sheet1.write(i+1,1,rating_list[i],set_sheetstyle('Microsoft YaHei',220,False))
    #     if inputdate_list[i]:
    #         sheet1.write(i+1,2,inputdate_list[i],set_sheetstyle('Microsoft YaHei',220,False))
    #     if comment_list[i]:
    #         sheet1.write(i+1,3,comment_list[i],set_sheetstyle('Microsoft YaHei',220,False))
    #     if intro_list[i]:
    #         sheet1.write(i+1,4,intro_list[i],set_sheetstyle('Microsoft YaHei',220,False))
        
    # workbook.save('collectMusic.xls')

user = config.User_id
if config.Book == True:
    grab_book(user)
if config.Movie == True:
    grab_data('movie',user)
if config.Music == True:
    grab_data('music',user)

    


    

