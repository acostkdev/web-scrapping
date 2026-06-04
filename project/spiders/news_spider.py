"""
Configuración de Scrapy para el proyecto.
"""

import scrapy


class NoticiaItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    published = scrapy.Field()
    summary = scrapy.Field()
    body = scrapy.Field()
    source = scrapy.Field()
    category = scrapy.Field()
    sentiment = scrapy.Field()


class RssSpider(scrapy.Spider):
    """
    Spider que parsea feeds RSS/Atom y extrae artículos.
    
    Uso:
        scrapy crawl rss -a urls_file=feeds.txt
        scrapy crawl rss -a urls="https://feed1,https://feed2"
    """
    name = "rss_spider"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (compatible; NewsMonitor/1.0)",
        "ROBOTSTXT_OBEY": False,
        "DOWNLOAD_DELAY": 1.0,
        "FEED_FORMAT": "jsonlines",
        "FEED_URI": "data/dataset_scrapy.jsonl",
    }
    
    def __init__(self, urls=None, urls_file=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = []
        
        if urls:
            self.start_urls = [u.strip() for u in urls.split(",")]
        elif urls_file:
            with open(urls_file) as f:
                self.start_urls = [line.strip() for line in f if line.strip()]
        else:
            self.start_urls = [
                "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/mexico/portada",
                "https://www.reddit.com/r/python/.rss",
                "https://hnrss.org/frontpage",
            ]
    
    def parse(self, response):
        """Parsea feed RSS/Atom y extrae cada artículo."""
        # intentar como RSS
        for item in response.xpath("//item"):
            article = {
                "title": item.xpath("title/text()").get(""),
                "link": item.xpath("link/text()").get(""),
                "published": item.xpath("pubDate/text()").get(""),
                "summary": item.xpath("description/text()").get(""),
                "source": response.url,
            }
            yield NoticiaItem(**article)
        
        # intentar como Atom
        for entry in response.xpath("//entry"):
            article = {
                "title": entry.xpath("title/text()").get(""),
                "link": entry.xpath("link/@href").get(""),
                "published": entry.xpath("published/text()").get(""),
                "summary": entry.xpath("summary/text()").get(""),
                "source": response.url,
            }
            yield NoticiaItem(**article)
