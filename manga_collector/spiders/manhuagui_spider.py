import scrapy
from scrapy.http import Response
from functools import partial

from manga_collector.items import MangaChapterItem


class ManHuaGuiSpider(scrapy.Spider):
    name = 'MHGSpider'
    start_urls = ['https://www.manhuagui.com/comic/7580/']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.out_dir = './out/'

    def parse(self, response):
        book_contents_url = ManHuaGuiSpider.start_urls[0]
        yield response.follow(book_contents_url, self.parse_book_contents)

    def parse_book_contents(self, response: Response):
        # get book name
        book = response.css('div.book-title h1').extract_first()

        # get version titles
        ver_titles = []
        for ver_title in response.css('div.chapter h4'):
            ver_titles.append(ver_title.css('::text').get())

        # get version chapter lists
        branchs = response.css('div.chapter div.chapter-list')
        for ver_title, ver_chapters in zip(ver_titles, branchs):
            chapter_no = 0
            for sub_chapter_list in ver_chapters.css('ul'):
                # lastest chapter appears in the front, reversed to
                # get an increase order chapter list
                for chapter in reversed(sub_chapter_list.css('li a')):
                    # <a href="/comic/xxxx/xxxxxx.html" title="第xx回" ...>
                    #   <span>第xx回<i>xxp</i></span>
                    # </a>
                    chapter_no += 1
                    chapter_url = chapter.css('::attr(href)').extract_first()
                    title, pages = chapter.css('::text').extract()
                    pages = int(pages[:-1])
                    chapter_item = MangaChapterItem({
                        'book': book,
                        'version': ver_title,
                        'chapter_no': chapter_no,
                        'title': title,
                        'pages': pages,
                        'chapter_url': chapter_url,
                        'store_dir': self.out_dir
                    })
                    yield chapter_item

                    # request for each page of chapter
                    for page in range(1, pages+1):
                        page_item = {
                            'chapter': dict(chapter_item),
                            'page_no': page
                        }

                        page_url = '%s#%d' % (chapter_url, page)
                        chapter_request = response.follow(
                            page_url, partial(self.parse_book_page, page_item))
                        yield chapter_request

    def parse_book_page(self, item, response: Response):
        img_url = response.css('div#mangaBox img::attr(src)').extract_first()
        item['img_url'] = img_url
        yield item
