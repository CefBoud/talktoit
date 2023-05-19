import glob
import os
import re
from pathlib import Path

import w3lib.html
# https://stackoverflow.com/a/47581199/11674997
from crochet import setup, wait_for
from scrapy.crawler import CrawlerRunner
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

import conf

from ..items import ScrapyCrawlerItem

setup()


class MySpider(CrawlSpider):
    name = "scrapy_crawler"
    # rules = (Rule(LinkExtractor(), callback="parse_item", errback="handle_errback", follow=True),)
    rules = (Rule(LinkExtractor(), callback="parse_item", follow=True),)

    def __init__(self, start_urls=[], domain="", max_pages=5, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.domain = domain
        self.allowed_domains = [self.domain]
        self.start_urls = start_urls if start_urls else [f"https://{domain}"]
        self.storage_dir = Path(f"{conf.DATA_DIR}/{domain}")

        self.parsed_item_count = 0
        self.max_pages = max_pages
        self.storage_dir.mkdir(exist_ok=True, parents=True)

    def parse_item(self, response):
        page = response.url.split("://")[1].replace("/", "__")
        filePath = self.storage_dir / Path(f"{page}.html")
        filePath.touch(exist_ok=True)
        content = w3lib.html.remove_tags_with_content(
            "".join(response.css("body *:not(script)::text").getall()),
            which_ones=("script",),
        )
        content = re.sub(r"\s+", " ", content)
        filePath.write_text(content)  # (response.body)
        self.log(
            f"Saved file {filePath},  self.parsed_item_count : { self.parsed_item_count}"
        )
        return ScrapyCrawlerItem(title=page)


def domain_is_scrapped(domain):
    storage_dir = Path(f"{conf.DATA_DIR}/{domain}")
    return len(glob.glob1(storage_dir, "*.html")) > 0


@wait_for(timeout=15.0)
def start_crawler(domain, start_urls=[], max_pages=5, success_callback=None):
    # clean old content if it exists
    for f in glob.glob(f"{conf.DATA_DIR}/{domain}/*.html"):
        os.remove(f)

    # https://stackoverflow.com/a/57567874/11674997
    settings = get_project_settings()
    settings = dict(settings) | {
        # "CLOSESPIDER_PAGECOUNT": max_pages,
        "CLOSESPIDER_ITEMCOUNT": max_pages,
        # https://github.com/scrapy/scrapy/issues/2748#issuecomment-302536094
        "CONCURRENT_REQUESTS": max_pages // 5,  # why 5? 🤷
    }
    configure_logging(settings)
    runner = CrawlerRunner(settings=settings)
    d = runner.crawl(MySpider, start_urls=start_urls, domain=domain)
    d.addCallback(
        lambda _: print("=========================================> crawl finished")
    )
    if success_callback:
        d.addCallback(success_callback)
    d.addErrback(lambda _: print("###### crawl callback error   ######"))

    return d
