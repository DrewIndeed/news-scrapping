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

def get_preview(article_link, preview_target, results):
    try:
        # suspicious statement so it needs error handling
        drilling_site = requests.get(article_link)

        # manipulate using BeautifulSoup
        soup_pot = BeautifulSoup(drilling_site.text, "html.parser")

        preview = soup_pot.select(preview_target)
        if len(preview) == 0:
            results.append("Click to discover further")
            return
        s = preview[0].getText()
        results.append(' '.join(s.split()))

    # error handling for connection failure
    except requests.exceptions.ConnectionError:
        # get the exception information
        error_type, error_obj, error_info = sys.exc_info()

        # print the link that cause the problem
        print('ERROR FOR LINK:', article_link)

        # print error info and line that threw the exception
        print(error_type, 'Line:', error_info.tb_lineno)

def indi_attack(full_url, soup_pot, both_belong_area, indi_part, title_target, img_target, container, preview_results):
    titles = soup_pot.select(both_belong_area + " " + indi_part + " " + title_target)
    imgs = soup_pot.select(both_belong_area + " " + indi_part + " " + img_target)
    run_by = titles if (len(titles) < len(imgs)) else imgs
    for i in range(len(run_by) - 1):
        if titles[i] and imgs[i]:
            clean_title = titles[i].getText().strip()
            link = titles[i]['href']
            img_link = ""
            if full_url == "https://www.marketwatch.com/investing/cryptocurrency":
                img_link = imgs[i]['data-srcset'].split(' ')[0]
            elif imgs[i].has_attr('data-src'):
                img_link = imgs[i]['data-src']
            container.append([clean_title, link, img_link])
            preview_results.append(link)

def scrap_both_belong(full_url, both_belong_area, indi_2, indi_1, title_target, img_target, container, preview_results):
    try:
        # suspicious statement so it needs error handling
        drilling_site = requests.get(full_url)

        # manipulate using BeautifulSoup
        soup_pot = BeautifulSoup(drilling_site.text, "html.parser")

        # target the scrapping area
        if indi_1 != "":
            indi_attack(full_url, soup_pot, both_belong_area, indi_1, title_target, img_target, container, preview_results)

        indi_attack(full_url, soup_pot, both_belong_area, indi_2, title_target, img_target, container, preview_results)


    # error handling for connection failure
    except requests.exceptions.ConnectionError:
        # get the exception information
        error_type, error_obj, error_info = sys.exc_info()

        # print the link that cause the problem
        print('ERROR FOR LINK:', full_url)

        # print error info and line that threw the exception
        print(error_type, 'Line:', error_info.tb_lineno)
