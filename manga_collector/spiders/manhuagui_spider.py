import scrapy


class ManHuaGuiSpider(scrapy.Spider):
    name = 'MHGSpider'
    start_urls = ['https://www.manhuagui.com/comic/7580/']

    def parse(self, response):
        # get version titles
        ver_titles = []
        for ver_title in response.css('div.chapter h4'):
            ver_titles.append(ver_title.css('::text').get())

        # get version
        branchs = response.css('div.chapter div.chapter-list')
        for ver_title, ver_chapters in zip(ver_titles, branchs):
            chapter_no = 1
            for sub_chapter_list in ver_chapters.css('ul'):
                # lastest chapter appears in the front, reversed to
                # get an increase order chapter list
                for chapter in reversed(sub_chapter_list.css('li a')):
                    # <a href="/comic/xxxx/xxxxxx.html" title="第xx回" ...>
                    #   <span>第xx回<i>xxp</i></span>
                    # </a>
                    url = chapter.css('::attr(href)').extract_first()
                    title, pages = chapter.css('::text').extract()
                    pages = int(pages[:-1])
                    yield {
                        'version': ver_title,
                        'chapter_no': chapter_no,
                        'title': title,
                        'pages': pages,
                        'url': url
                    }
                    chapter_no += 1

    def parse_book_contents(self, response):
        pass
