# Douban_backup
备份豆瓣用户看（听）过的书、影、音（请勿暴力爬虫），以图书为例，同步看过的书名、打分和短评。
豆瓣音乐暂时无法同步短评。

用法：
在config.py中指定用户id。用户id可以从豆瓣个人主页的网址获得，如id为'ahbei'的用户，其个人主页为"https://www.douban.com/people/ahbei/"
运行grab.py即可。

环境：
python 3.6; 
需要：codecs; bs4 (BeautifulSoup); xlwt
