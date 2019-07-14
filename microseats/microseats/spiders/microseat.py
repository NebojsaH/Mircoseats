# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request


class MicroseatSpider(scrapy.Spider):
    name = 'microseat'
    allowed_domains = ['mircoseats.com']
    start_urls = ['https://mircoseats.com/k5,dedicated-mountings.html',
                  'https://mircoseats.com/k5,dedicated-mountings,2.html',
                  'https://mircoseats.com/k5,dedicated-mountings,3.html',
                  'https://mircoseats.com/k5,dedicated-mountings,4.html',
                  'https://mircoseats.com/k5,dedicated-mountings,5.html',
                  'https://mircoseats.com/k5,dedicated-mountings,6.html',
                  'https://mircoseats.com/k5,dedicated-mountings,7.html',
                  'https://mircoseats.com/k5,dedicated-mountings,8.html']

    def parse(self, response):
        link = response.xpath('//*[@class="main__product-wrapper"]/a/@href').extract()


        for l in link:
            absolute_l = response.urljoin(l)
            yield Request(absolute_l, callback=self.parse_sediste)
        next_page_url = response.xpath('//*[@class="main__pagination"]/a/@href').extract()
        next_page_url2 = next_page_url[1]
        next_absolute = response.urljoin(next_page_url2)
        yield Request(next_absolute, callback=self.parse)

    def parse_sediste(self, response):
        ime = response.css('h1::text').extract_first()
        kratki_opis = response.xpath('//*[@class="main__product-page-short-description"]/text()').extract_first()
        sku = response.xpath('//*[@class="main__product-code"]/text()').extract_first()
        cena = response.xpath('//*[@class="main__product-page-pricing--included"]/text()').extract_first()
        opis = "".join(line for line in response.xpath('//*[@class="main__product-page-description"]/div/text()').extract())
        slike = response.xpath('//*[@class="main__product-page-gallery"]//img/@src').extract()
        slike_link = [response.urljoin(slikea) for slikea in slike]
        slike = [slika.replace('_m', '') for slika in slike_link]
        features = " ".join(line for line in response.xpath('//*[@class="main__product-features-list-item"]/span/text()').extract())

        yield {
            'Ime': ime,
            'Kratki opis': kratki_opis,
            'SKU': sku,
            'Cena': cena,
            'Opis': opis,
            'Slike': slike,
            'Features': features
        }

