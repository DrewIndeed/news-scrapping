import re
import sys
import threading
import time

import requests
from bs4 import BeautifulSoup


def get_domain(full_url):
    """
    :param full_url: complete source urls
    :return: only domain of url: String
    """
    rs = re.match("https://(.*?)/", full_url)
    return rs.group(0)[:-1]


def scrap(full_url, news_area, target_container):
    """
    :param full_url: full url of the currently scrapping site
    :param news_area: the container/list of articles
    :param target_container: container list for all results after running multithreading
    :return: void
    """

    # store temporary results
    scrap_result = []
    try:
        # suspicious statement so it needs error handling
        drilling_site = requests.get(full_url)

        # manipulate using BeautifulSoup
        soup_pot = BeautifulSoup(drilling_site.text, "html.parser")

        # target the scrapping area
        peek_agent = soup_pot.select(news_area)

        # extract title and link <a> tag
        for peek_item in peek_agent:
            for article in peek_item.find_all('a'):
                link = article['href']
                title = article.getText()
                if get_domain(full_url) not in link:
                    link = get_domain(full_url) + link
                if title == '':
                    continue

                # put into temporary container
                scrap_result.append({"source": get_domain(full_url), "title": title.strip(), "link": link})

    # error handling for connection failure
    except requests.exceptions.ConnectionError:
        # get the exception information
        error_type, error_obj, error_info = sys.exc_info()

        # print the link that cause the problem
        print('ERROR FOR LINK:', full_url)

        # print error info and line that threw the exception
        print(error_type, 'Line:', error_info.tb_lineno)

    # appending into external final container
    target_container += scrap_result

# main program
if __name__ == "__main__":
    # sources and their scrapping area
    # src 1
    economic_times = "https://economictimes.indiatimes.com/markets/cryptocurrency"
    eco_top_news = "div.story_sec"
    eco_sub_news = "ul.newsSec li"
    # src 2
    money_control = "https://www.moneycontrol.com/news/tags/cryptocurrency.html/news/"
    money_news = "#cagetory li.clearfix"
    # src 3
    market_watch = "https://www.marketwatch.com/investing/cryptocurrency"
    market_news = ".article__content .article__headline"
    # src 4
    investopedia = "https://www.investopedia.com/cryptocurrency-news-5114163"
    investopedia_top_news = ".comp.spotlight.mntl-block"
    investopedia_sub_news = ".comp.taxonomy-cards.mntl-block"

    # result container
    crypto_articles = []

    # task container
    thread_pool = [threading.Thread(target=scrap, args=(economic_times, eco_top_news, crypto_articles)),
                   threading.Thread(target=scrap, args=(economic_times, eco_sub_news, crypto_articles)),
                   threading.Thread(target=scrap, args=(money_control, money_news, crypto_articles)),
                   threading.Thread(target=scrap, args=(market_watch, market_news, crypto_articles)),
                   threading.Thread(target=scrap, args=(investopedia, investopedia_top_news, crypto_articles)),
                   threading.Thread(target=scrap, args=(investopedia, investopedia_sub_news, crypto_articles))]

    # Capture threading start time
    start_time = time.perf_counter()

    # start threads
    for thread in thread_pool:
        thread.start()

    # end thread when completed
    for thread in thread_pool:
        thread.join()

    # Capture threading execution time
    end_time = time.perf_counter()
    execution_time = end_time - start_time

    # [TEMPORARY]: print out the result; [FUTURE TARGET]: store in database
    for item in crypto_articles:
        print(item)

    # program performace check
    print('\nCheckmark: ' + str(len(crypto_articles)) + " articles in " + str(round(execution_time, 2)) + " secs")
    print(f'Average total time: {round(execution_time / 6, 2)} secs per thread')
