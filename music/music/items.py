# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MusicItem(scrapy.Item):
    # define the fields for your item here like:
    # name=scrapy.Field()
    choice=scrapy.Field()#用户输入的功能选择
    music=scrapy.Field()#歌曲链接列表
    music_name=scrapy.Field()#歌曲名列表
    songs_name=scrapy.Field()#流行歌曲名列表
    songs_url=scrapy.Field()#流行歌曲链接列表
    your_search=scrapy.Field()#选择的歌手，未下载歌手列表
    your_search_num=scrapy.Field()#选择下载数量
    down_songs_num=scrapy.Field()#下载流行音乐数量
    your_search_download=scrapy.Field()#已下载歌手列表
    # file_urls=scrapy.Field()
    # flies=scrapy.Field()
