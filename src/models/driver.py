import os
import traceback

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

from models.org_log import Log

_EXEC_FILE_NAME = os.path.basename(__file__)[:-3]


class NoneElementsError(Exception):
    """ None Elements Error """


class Driver(object):
    def __init__(self, url="https://www.google.co.jp/", headless=False):
        """Default: Google Chrome
          params:
            url(str): search target url
        """
        self.log = Log(logger_name=_EXEC_FILE_NAME)
        self.log.logger.info('init ...')

        self.headless = headless
        self.driver = self._set_chrome_option()
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get(url)

        self.log.logger.info({'url': url})
        self.log.logger.info('init end')

    def _set_chrome_option(self):
        """ISSUES:
        Chrome Option

        """
        options = Options()
        options.add_argument('--window-size=640,1024')

        if self.headless:
            # docker, linux etc
            # options.binary_location = '/usr/bin/google-chrome'
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            chrome_service = service.Service(executable_path='/usr/bin/chromedriver')
            ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) '
            ua += 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
            options.add_argument(f"user-agent={ua}")
            driver = webdriver.Chrome(service=chrome_service, options=options)
        else:
            chrome_service = service.Service(executable_path='/usr/local/bin/chromedriver')
            driver = webdriver.Chrome(service=chrome_service, options=options)

        return driver

    def close(self):
        self.driver.close()
        self.driver.quit()
        self.log.logger.info('done')

    def search_query(self, by_class_name='gLFyf', query=None, sleep_=5) -> None:
        """ 指定文字列で検索し Enter

        params:
          by_class_name(str): 検索タグのクラス名, default: gLFyf (Google)
          query(str)     : 検索文字列, default: None
          sleep_(int)    : 処理間隔 (sec)
        """

        try:
            elements = self.wait.until(lambda x: x.find_elements(By.CLASS_NAME, by_class_name))
            self.log.logger.debug({f"elements: {elements}"})

            if not elements:
                raise NoneElementsError

            if query:
                event = {"element": elements[0]}
                self.log.logger.info(f"search query: {query}")
                event["element"].send_keys(query)
                event["element"].send_keys(Keys.ENTER)
                self.driver.implicitly_wait(20)
                # 入力値 clear
                self.clear_search_box()

        except NoneElementsError:
            self.log.logger.error('None elements Error ...')
            self.close()
        except Exception as ex:
            self.log.logger.error({f"'ex: '{ex}"})
            self.log.logger.error(traceback.format_exc())
            self.close()

    def second_over_search_query(self, *args, **keywords) -> None:
        pass

    def clear_search_box(self, *args, **keywords) -> None:
        pass

    def send_key(self, xpath, send_key):
        """tag 要素を当てて入力する

        params:
          xpath(str)
          send_key(str)

        """
        elements = self.wait.until(lambda x: x.find_elements(By.XPATH, xpath))
        event = {"element": elements[0]}
        event["element"].send_keys(send_key)

    def click_bottom(self, xpath):
        """ tag 要素を当てて click """
        elements = self.wait.until(lambda x: x.find_elements(By.XPATH, xpath))
        sleep(3)
        self.driver.execute_script("arguments[0].click();", elements[0])

    def assert_title_check(self, title=None):
        """ 現在のページのタイトルをチェック """
        assert self.driver.title == title
        self.log.logger.info({'msg': f"{title} OK"})


class YahooBrowser(Driver):

    def __init__(self, url='https://www.yahoo.co.jp'):
        super().__init__(url=url)

    def second_over_search_query(self, by_class_name='SearchBox__searchInput', query=None, sleep_=3) -> None:
        """ 検索文字列入力 2回目以降 """
        elements = self.wait.until(lambda x: x.find_elements(By.CLASS_NAME, by_class_name))

        event = {"element": elements[0]}
        self.log.logger.info(f"search query: {query}")
        event["element"].send_keys(query)
        event["element"].send_keys(Keys.ENTER)
        sleep(sleep_)
        self.clear_search_box()

    def clear_search_box(self, by_class_name='SearchBox__clearButton', sleep_=3) -> None:
        """ 検索文字列を削除 """
        elements = self.driver.find_elements(By.CLASS_NAME, by_class_name)
        event = {"element": elements[0]}
        self.log.logger.debug({f"elements: {elements}"})
        event["element"].send_keys(Keys.ENTER)
        self.log.logger.info({f"msg: cleared search box"})

        sleep(sleep_)
