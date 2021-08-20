import threading
import time
from supporters import *

# main program
if __name__ == "__main__":
    # sources and their scrapping area
    # src 1
    economic_times = "https://economictimes.indiatimes.com/markets/cryptocurrency"
    eco_top_news = "div.story_sec"
    eco_sub_news = "ul.newsSec li"
    eco_img = ".artImg img"
    eco_prev = "artText"
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
    t1 = threading.Thread(target=scrap_title_link, args=(economic_times, eco_top_news, crypto_articles))
    t2 = threading.Thread(target=scrap_title_link, args=(economic_times, eco_sub_news, crypto_articles))
    t3 = threading.Thread(target=scrap_title_link, args=(money_control, money_news, crypto_articles))
    t4 = threading.Thread(target=scrap_title_link, args=(market_watch, market_news, crypto_articles))
    t5 = threading.Thread(target=scrap_title_link, args=(investopedia, investopedia_top_news, crypto_articles))
    t6 = threading.Thread(target=scrap_title_link, args=(investopedia, investopedia_sub_news, crypto_articles))

    # Capture threading start time
    start_time = time.perf_counter()
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()

    # Capture threading execution time
    end_time = time.perf_counter()
    execution_time = end_time - start_time

    # [TEMPORARY]: print out the result; [FUTURE TARGET]: store in database
    for item in crypto_articles:
        print(item)

    # program performace check
    print('\nCheckmark: ' + str(len(crypto_articles)) + " articles in " + str(round(execution_time, 2)) + " secs")
    print(f'Average total time: {round(execution_time / 6, 2)} secs per thread')
