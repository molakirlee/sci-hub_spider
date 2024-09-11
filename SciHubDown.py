# -*- coding: utf-8 -*-
#      Python 3.6           



import requests
from bs4 import BeautifulSoup
import os,re
import time,random

Info = '''
##############################################
#                                            #
#  X   X   I   L        OO      CCC   K  K   # 
#   X X    I   L       O  O    C      K K    # 
#    X     I   L      O    O  C       KK     # 
#   X X    I   L       O  O    C      K K    # 
#  X   X   I   LLLLLL   OO      CCC   K  K   # 
#                                            #
#   Non-commercial or personal use only.     #
#          "To achieve oneself               #
#        is to help others achieve"          # 
#              By  Xilock                    #
#           update 11 Sep 2024               #
#             version: 2.0                   #
#         Created by 19 Jan 2022             #
##############################################
'''
print(Info)

path = ".\\Download_PDF\\"
if os.path.exists(path) == False:
 os.mkdir(path)
if os.path.exists("error.txt") ==True:
 os.remove("error.txt")
f = open("doi.txt", "r", encoding="utf-8")  #存放DOI码的.txt文件中，每行存放一篇参考文献
fsite = open('scihubSite.txt', "r", encoding="utf-8") #存放scihub网站地址的.txt文件
scihubSite = fsite.readline()
fsite.close()
head = {\
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'\
            }  #20210607更新，防止HTTP403错误
err_num = 0
soup_num = 0
 
def Download(url,title,doi):
 file = path + title + ".pdf"
 # 对于有的sci地址而言，会在右侧显示出文章的预览，而有的不会，这里分别处理这两种情况。
 if os.path.exists(file) == False:
  r = requests.get(url, headers=head)
  r.raise_for_status()
  r.encoding = r.apparent_encoding
  soup = BeautifulSoup(r.text, "html.parser")
#  download_url = "https://sci.bban.top/pdf/" + doi + ".pdf#view=FitH"
#  download_url = soup.embed.attrs["src"]
  try:
    download_url = soup.iframe.attrs["src"]
  except:
    # download_url = "https:" + soup.embed.attrs["src"]
    download_url = soup.embed.attrs["src"]
  print(doi + " is downloading...\n  --The download url is: " + download_url)
#  
  download_r = requests.get(download_url, headers=head)
  download_r.raise_for_status()

  with open(file, "wb+") as temp:
   temp.write(download_r.content)
   print("<" + title + ".pdf> downloaded!")
 else:
  print("<" + title + ".pdf> already exists!")

# Main 
for line in f.readlines():
 time.sleep(random.randint(15, 60)) # 随机的隔一段时间下载，防止被封ip地址，这里设置的是15 到60秒之间的随机数
 line = line[:-1] #去换行符
 title = line.split('|')[0]
 doi_pattern = 'doi:.+'
# if (len(re.findall(doi_pattern, line)) != 0):
 if (len(line) != 0):
  doi = line.split('|')[1]
#  url = "https://www.sci-hub.ren/doi:" +doi + "#"
#  url = "https://www.sci-hub.ren/" +doi + "#" # failed without "#"
  url = scihubSite +doi + "#" # failed without "#"
#  url = "www.sci-hub.ren/" +doi
#  url = "https://sci-hub.se/" +doi
  print(url)
  try:
#   Download(url,author_date)
   Download(url,title,doi)
  except:
   err_num = err_num + 1
   with open("error.txt", "a+", encoding="utf-8") as error:
    error.write(str(err_num) + "." + line + " occurs error!\n --download_url may be:\n" + url + "\n")
   print(line + "\n" + "Failed to download!!!")
 else:
  print(line + "\n"+"doi not found,failed to download!!!")
  err_num = err_num + 1
  with open("error.txt", "a+", encoding="utf-8") as error:
   error.write(str(err_num) + "." + line + " occurs error!\n")
f.close()
