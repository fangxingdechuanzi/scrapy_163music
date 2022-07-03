# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import requests
from selenium import webdriver

class MusicPipeline:
    def open_spider(self,spider):
        pass
    def close_spider(self,spider):
        pass
    def process_item(self, item, spider):
        root = 'D:/Music163'
        if not os.path.exists(root):
            os.mkdir(root)
        header1 = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"
        }
        # webpags = webdriver.ChromeOptions()
        # webpags.add_argument('--headless')
        # webpage = webdriver.Chrome(options=webpags)
        if item['choice'] == '1':
            file2=root+'/流行歌曲'
            if not os.path.exists(file2):
                os.mkdir(file2)
            for i in range(len(item['songs_name'])):
                webpags = webdriver.ChromeOptions()
                webpags.add_argument('--headless')
                webpage = webdriver.Chrome(options=webpags)
                path2=file2+'/'+item['songs_name'][i]+'.mp3'
                song_url=item['songs_url'][i]
                print(path2,song_url)
                if not os.path.exists(path2):
                    try:
                        webpage.get(song_url)
                        url2=webpage.current_url
                        webpage.close()
                        song2=requests.get(url2,headers=header1)
                        with open(path2,'ab') as f2:
                            f2.write(song2.content)
                        print(item['songs_name'][i],'已下载到D:/Music163/')
                    except:
                        print(item['songs_name'][i],'不能下载')
        elif item['choice']=='2':
            file=root+'/'+item['your_search'][-1]
            if not os.path.exists(file):
                os.mkdir(file)
            for j in range(len(item['music_name'])):
                webpags = webdriver.ChromeOptions()
                webpags.add_argument('--headless')
                webpage = webdriver.Chrome(options=webpags)
                path=file+'/'+item['music_name'][j]+'.mp3'
                url_song=item['music'][j]
                if not os.path.exists(path):
                    try:
                        webpage.get(url_song)
                        url = webpage.current_url
                        webpage.close()
                        song = requests.get(url, headers=header1)
                        with open(path, 'ab') as f:
                            f.write(song.content)
                        print(item['music_name'][j],'已下载到D:/Music163/')
                    except:
                        print(item['music_name'][j], '不能下载')
            # print(item['your_search'],'名字有误，请按照某易云音乐的歌手名字输入')
        else:
            pass
        return item
