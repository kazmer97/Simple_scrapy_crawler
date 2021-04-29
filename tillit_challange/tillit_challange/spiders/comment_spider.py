import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tillit_challange.items import TillitChallangeItem


class MySpider(CrawlSpider):

    def __init__(self, domain = 'https://news.ycombinator.com,https://news.ycombinator.com/newcomments'):
        self.start_urls = [i for i in domain.split(',')]

    # The name of the spider
    name = "ycomb"

    # The domains that are allowed (links to other domains are skipped)
    allowed_domains = ["ycombinator.com"]

    # The URLs to start with
    # start_urls = ["https://news.ycombinator.com", "https://news.ycombinator.com/newcomments"]

    # This spider has one rule: extract all (unique and canonicalized) links, follow them and parse them using the parse_items method
    rules = [
        Rule(
            LinkExtractor(
                canonicalize=False,
                unique=True
            ),
            follow=True,
            callback="parse_items"
        )
    ]

    # Method which starts the requests by visiting all URLs specified in start_urls
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    # Method for parsing items
    def parse(self, response):
        # The list of items that are found on the particular page
        items = []
        # Only extract canonicalized and unique links (with respect to the current page)
        links = LinkExtractor(canonicalize=False, unique=True).extract_links(response)
        # Now go through all the found links
        
        for link in links:
            item = TillitChallangeItem()
            item['url_from'] = response.url
            item['url_to'] = link.url
            with open("links.txt", 'a+') as output:
                output.write( "".join([item['url_from'], " --> ", item['url_to'],"\n"]))
            items.append(item)

        # Return all the found items
        return items