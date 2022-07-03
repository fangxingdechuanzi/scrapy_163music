import scrapy
from music.items import MusicItem

class Savemp3Spider(scrapy.Spider):
    name = 'saveMp3'
    allowed_domains = ['music.163.com']
    base_urls = 'https://music.163.com'
    base_song_urls = 'https://music.163.com/song/media/outer/url?id={}.mp3 '#音乐链接模板
    item = MusicItem()

    def start_requests(self):
        print('本程序禁止商用，未经许可禁止传播，违反以上要求，后果自负！！！')
        print('欢迎进入网易云音乐批量下载程序，不用充VIP哦>(--)<')
        choice=input('输入‘1’下载最新流行歌曲，输入‘2’下载指定歌手的歌曲，输入其他字符退出：')
        self.item['choice']=choice
        if choice =='1':
            down_songs_num=input('输入你要下载歌曲的数量(正整数)：')
            pop_music_web_url=self.base_urls+'/discover/toplist/'
            self.item['down_songs_num']=down_songs_num
            yield scrapy.Request(pop_music_web_url,callback=self.parse_song_id)
        elif choice == '2':
            your_search = input('输入你要搜索的歌手：')
            your_search_num = input('请输入你要下载歌曲的数量(正整数)：')
            your_search_url=self.base_urls+'/discover/artist/'
            self.item['your_search']=your_search.split('0')
            self.item['your_search_download']=[]#已下载歌手列表
            self.item['your_search_num']=your_search_num
            yield scrapy.Request(your_search_url)
            # yield scrapy.Request(your_search_url,callback=self.parse)

    #获取歌手分类页面的链接
    def parse(self, response):
        singer_type=response.css('#singer-cat-nav div')
        for singer in singer_type:
            singer_type_url=singer.css('ul li')
            for type_url in singer_type_url:
                singers_url=type_url.css('a::attr(href)').extract()[0]
                url=self.base_urls+singers_url
                yield scrapy.Request(url,callback=self.parse_singer_id)

    #找出所有歌手、歌单链接，字典形式,把用户输入的歌手页面链接输出
    def parse_singer_id(self,response):
        user_choices=self.item['your_search']
        # print(user_choice)
        artist_dic={}
        artist_list=response.css('#m-artist-box li')
        for arts in artist_list:
            artist=arts.css('a::text').extract()[0]
            artist_url=arts.css('a::attr(href)').extract()[0]
            artist_dic[artist]=artist_url
        # print('热门歌手集合：',artist_dic.keys())
        for user_choice in user_choices:
            if user_choice in artist_dic:
                # print(artist_dic[user_choice])
                singer_url=self.base_urls+artist_dic[user_choice]#歌手页面链接
                # self.item['your_search_download'].append(user_choice)#已下载歌手列表
                # self.item['your_search'].remove(user_choice)#删除已下载的歌手
                yield scrapy.Request(singer_url,callback=self.get_songs_url)
            else:
                continue

    #得到歌名和.mp3链接所有信息储存在self.item中
    def get_songs_url(self,response):
        self.item['music_name'] = []
        self.item['music'] = []
        print(response.url)
        user_choice_num=int(self.item['your_search_num'])
        # print(user_choice_num)
        songs_list=response.css('ul.f-hide>li')
        num=0
        for i in songs_list:
            num+=1
            if user_choice_num >= num:
                song_name = i.css('a::text').extract()[0]
                song_url=i.css('a::attr(href)').extract()[0]
                url_id=song_url.split('=')[1]
                mp3_url=self.base_song_urls.format(url_id)
                self.item['music_name'].append(song_name)
                self.item['music'].append(mp3_url)
                # print(self.item)
                # yield self.item
        return self.item

    #**********下载流行音乐************
    def parse_song_id(self,response):
        down_num=int(self.item['down_songs_num'])
        num=0
        self.item['songs_url']=[]
        self.item['songs_name']=[]
        pop_songs_list=response.css('ul.f-hide>li')
        for songs_id_list in pop_songs_list:
            num+=1
            if down_num >= num:
                songs_id=songs_id_list.css('a::attr(href)').extract()[0]
                songs_name=songs_id_list.css('a::text').extract()[0]
                # print(songs_name,songs_id)
                url_id=songs_id.split('=')[1]
                songs_url=self.base_song_urls.format(url_id)
                self.item['songs_url'].append(songs_url)
                self.item['songs_name'].append(songs_name)
        # print(self.item)
        return self.item


