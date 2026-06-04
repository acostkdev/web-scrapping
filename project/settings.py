BOT_NAME = "news_monitor"
SPIDER_MODULES = ["spiders"]
NEWSPIDER_MODULE = "spiders"
ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 1.0
USER_AGENT = "Mozilla/5.0 (compatible; NewsMonitor/1.0)"
FEED_FORMAT = "jsonlines"
