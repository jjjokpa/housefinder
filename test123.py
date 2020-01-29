import scrapy

class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ['http://search.danawa.com/dsearch.php?query=2070%20super&originalQuery=2070%20super&cate_c1=861&cate_c2=876&volumeType=allvs&page=1&limit=30&sort=saveDESC&list=list&boost=true&addDelivery=N&tab=main&tab=main']

    def parse(self, response):
        SET_SELECTOR = '.prod_item'
        print(response.css(SET_SELECTOR))
        
        # for brickset in response.css(SET_SELECTOR):
            # NAME_SELECTOR = 'a ::text'
            # yield {
            #     'name': brickset.css(NAME_SELECTOR).extract_first(),
            # }