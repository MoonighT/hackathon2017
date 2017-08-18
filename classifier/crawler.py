import os
import time
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

IMPLICITLY_WAIT = 10  # 10 seconds


class WebRunner(object):
    def __init__(self, phantomjs_path=None):
        super(WebRunner, self).__init__()

        caps = DesiredCapabilities.PHANTOMJS
        caps['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'

        if phantomjs_path:
            self.driver = webdriver.PhantomJS(executable_path=phantomjs_path, service_log_path=os.path.devnull)
        else:
            self.driver = webdriver.PhantomJS(service_log_path=os.path.devnull)
        self.driver.set_window_size(width=1920, height=1080)
        self.driver.implicitly_wait(IMPLICITLY_WAIT)

    def load_url(self, url):
        self.driver.get(url)

    def close(self):
        self.driver.close()


class Gender(object):
    MALE = 'male'
    FEMALE = 'female'


class Outfit(object):
    TOP = 'top'
    BOTTOM = 'bottom'


class Occasion(object):
    INTERVIEW = 'interview'
    BEACH = 'beach'


KEYWORDS = {
    Gender.MALE: [
        'male',
        'men',
    ],
    Gender.FEMALE: [
        'female',
        'women',
        'girl',
    ],
    Outfit.TOP: [
        'shirt',
    ],
    Outfit.BOTTOM: [
        'pants',
    ],
    Occasion.INTERVIEW: [
        'formal',
    ],
    Occasion.BEACH: [
        'casual',
    ]
}

KEYWORD_CONTEXT = [
    'wear',
]

DATA_SET = []

for gender in [Gender.MALE, Gender.FEMALE]:
    for outfit in [Outfit.TOP, Outfit.BOTTOM]:
        for occasion in [Occasion.INTERVIEW, Occasion.BEACH]:
            DATA_SET.append([gender, outfit, occasion])

RUNNER = WebRunner()


def keyword_combinations(data_set):
    combinations = []
    # for k_context in KEYWORD_CONTEXT:
    for k_gender in KEYWORDS.get(data_set[0]):
        for k_outfit in KEYWORDS.get(data_set[1]):
            for k_ocassion in KEYWORDS.get(data_set[2]):
                keywords = (k_gender, k_outfit, k_ocassion)
                combinations.append(keywords)

    return combinations


def pinterest_crawler(keywords):
    RUNNER.load_url('https://www.pinterest.com/search/pins/?q=%s' % ('%20'.join(keywords)))

    page_size = 0
    no_more_times = 0
    while True:
        RUNNER.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.1)
        curren_page_size = len(RUNNER.driver.page_source)
        print curren_page_size
        if curren_page_size > page_size:
            page_size = curren_page_size
            no_more_times = 0
        else:
            no_more_times += 1
            if no_more_times >= 20:
                break
    elements = RUNNER.driver.find_elements_by_xpath('//div[@class="GrowthUnauthPinImage"]//img')
    urls = [element.get_attribute('src') for element in elements]
    print len(urls)

    return urls


def amazon_crawler(keywords):
    page = 1
    urls_set = set()
    while True:
        host_url = 'https://www.amazon.com/s/field-keywords=%s&page=%s' % ('+'.join(keywords), page)
        RUNNER.load_url(host_url)
        elements = RUNNER.driver.find_elements_by_xpath('//img[@class="s-access-image cfMarker"]')
        if not elements:
            break
        page += 1
        urls = [element.get_attribute('src') for element in elements]
        for url in urls:
            urls_set.add(url)
    return urls_set


if __name__ == '__main__':
    for data_set in DATA_SET:
        print data_set
        with open('%s.txt' % '_'.join(data_set), 'a') as of:
            url_set = set()
            for keywords in keyword_combinations(data_set):
                print keywords
                urls = pinterest_crawler(keywords)
                for url in urls:
                    url_set.add(url)
            of.writelines('\n'.join(url_set))

    RUNNER.close()
