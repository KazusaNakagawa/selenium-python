import json
from time import sleep
from dotenv import load_dotenv
from models.driver import (
    Driver,
    YahooBrowser,
)

load_dotenv()

json_crawl = json.load(open('./conf/crawl.json', 'r'))


def yahoo_main():
    yb = YahooBrowser()
    queries = ['きょうの料理', 'ChatGTP おすすめ']
    try:
        for idx, query in enumerate(queries):
            if idx == 0:
                yb.search_query(by_class_name='_1wsoZ5fswvzAoNYvIJgrU4', query=query)
            else:
                yb.second_over_search_query(query=query)

    except Exception as ex:
        yb.log.logger.error(ex)
        yb.close()
    finally:
        yb.close()
        yb.log.logger.info('main end')


def login_site_main(target_id='id0001'):
    target_id = json_crawl[0][target_id]
    site = target_id['site']
    account = target_id['account']
    xpath = site['xpath']

    driver = Driver(url=site['url'], headless=True)
    try:
        driver.assert_title_check(title=site['login_title'])
        driver.send_key(xpath=xpath['email'], send_key=account['email'])
        driver.send_key(xpath=xpath['password'], send_key=account['password'])
        driver.click_bottom(xpath=xpath['loginButton'])
        sleep(5)
        driver.assert_title_check(title=site['home_title'])

    except Exception as ex:
        driver.log.logger.error(ex)
        driver.close()
    finally:
        driver.close()
        driver.log.logger.info('main end')


def login_site2_main(target_id='id0002'):
    target_id = json_crawl[0][target_id]
    site = target_id['site']
    account = target_id['account']
    xpath = site['xpath']

    driver = Driver(url=site['url'], headless=True)

    try:
        driver.assert_title_check(title=site['login_title'])
        driver.send_key(xpath=xpath['company'], send_key=account['company'])
        driver.send_key(xpath=xpath['email'], send_key=account['email'])
        driver.send_key(xpath=xpath['password'], send_key=account['password'])
        driver.click_bottom(xpath=xpath['loginButton'])
        sleep(5)
        driver.assert_title_check(title=site['home_title'])

    except Exception as ex:
        driver.log.logger.error(ex)
        driver.close()
    finally:
        driver.close()
        driver.log.logger.info('main end')


if __name__ == '__main__':
    # login_site_main()
    # login_site2_main()
    yahoo_main()
