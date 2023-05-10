import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            book_page = book.css('h3 a').attrib['href']
            if book_page is not None:
                if 'catalogue/' in book_page:
                    book_url = 'https://books.toscrape.com/'+ book_page
                else:
                    book_url = 'https://books.toscrape.com/catalogue/'+ book_page

                yield response.follow(book_url, callback=self.parse_book)


    def parse_book(self,response):
        table_rows = response.css('table tr')
        yield{
            'title': response.css(" .product_main h1::text ").get(),
            'description': response.xpath('//div[@id="product_description"]/following-sibling::p/text()').get(),
            'category': response.xpath('//ul[@class="breadcrumb"]/li[@class="active"]/preceding-sibling::li[1]/a/text()').get(),
            'rating': response.css(".star-rating ::attr(class)").get(),
            'Availability':table_rows[5].css('td ::text').get(),
            'Num_reviews':table_rows[6].css('td ::text').get(),
            'product_type':table_rows[1].css('td ::text').get(),
            'Price (excl. tax)': table_rows[2].css('td :: text').get(),
            'Price (incl. tax)' : table_rows[3].css('td :: text').get(),
            'price': response.css('.price_color ::text').get()
            }
        