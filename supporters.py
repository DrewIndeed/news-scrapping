import re
import sys
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