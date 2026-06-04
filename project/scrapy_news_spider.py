"""
scrapy_news_spider.py
Configuración de Scrapy para el proyecto SIMANW.

Uso:
    scrapy runspider scrapy_news_spider.py
    scrapy runspider scrapy_news_spider.py -a urls="https://feed1,https://feed2"
"""

from spiders.news_spider import NoticiaItem, RssSpider

__all__ = ["NoticiaItem", "RssSpider"]
