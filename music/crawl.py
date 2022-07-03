#scrapy启动文件
from scrapy import cmdline

cmdline.execute(['scrapy', 'crawl', 'saveMp3','--nolog'])
# cmdline.execute(['scrapy', 'crawl', 'saveMp3'])