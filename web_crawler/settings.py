######################################################################################################
#  Scrapy Settings
######################################################################################################

BOT_NAME = 'web_crawler'

SPIDER_MODULES = ['web_crawler.spiders']
NEWSPIDER_MODULE = 'web_crawler.spiders'

#DOWNLOAD_HANDLERS = {'s3': None,}
LOG_LEVEL = 'DEBUG'

DOWNLOAD_DELAY = 0.5
RANDOMIZE_DOWNLOAD_DELAY = True
DOWNLOAD_TIMEOUT = 160

LOCAL_FILES_PATH = '/data/crawler_data'

USER_AGENT_LIST = [
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',

    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0) Gecko/16.0 Firefox/16.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, '
    'like Gecko) Version/5.1.3 Safari/534.53.10',
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; "
    "Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; "
    ".NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; "
    ".NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; "
    ".NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; "
    "InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, "
    "like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) "
    "Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
]


DOWNLOADER_MIDDLEWARES = {
    'web_crawler.middlewares.RandomUserAgentMiddleware': 400,
    'web_crawler.middlewares.ProxyMiddleware': 410,
    'scrapy.downloadermiddleware.useragent.UserAgentMiddleware': None,
}

# DOWNLOADER_MIDDLEWARES = {
#     'web_crawler.middlewares.SeleniumMiddleware': 200
# }

#####################################################################################################
# S3 Credential
#####################################################################################################

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

######################################################################################################
# CSV Rules
######################################################################################################
CSV_DELIMITER = ","
CSV_QUOTECHAR = '"'
CSV_ESCAPECHAR= "\\"
FEED_EXPORTERS = {
    'csv': 'web_crawler.csv_pipeline.CSVPipeline',
}
FEED_FORMAT = 'csv'

######################################################################################################
# SQL Connection
######################################################################################################
SQL_HOST = ''

SQL_USER = ''
SQL_PASSWORD = ''


COOKIES_DEBUG = True



######################################################################################################
#
######################################################################################################

try:
   from local_settings import *
except ImportError:
   pass


if __name__ == "__main__" :

    print ('SQL_HOST: ' + SQL_HOST)
    print ('SQL_USER: ' + SQL_USER)
    print ('SQL_PASSWORD: ' + SQL_PASSWORD)
    print ('cred: ' + AWS_ACCESS_KEY_ID)
