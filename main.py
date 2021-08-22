import time
from supporters import *

# main program
if __name__ == "__main__":
    # sources and their scrapping areas
    # src 1
    money_control = "https://www.moneycontrol.com/news/tags/cryptocurrency.html/news/"
    money_news = "#cagetory"
    money_indi_1 = ""
    money_indi_2 = ".clearfix"
    money_img = "a img"  # data-src
    money_title = "h2 a"
    money_preview = ".article_desc"

    # src 2
    market_watch = "https://www.marketwatch.com/investing/cryptocurrency"
    market_news = ".region.region--primary"
    market_indi_1 = ".component.component--layout.layout--D4"
    market_indi_2 = ".component.component--module.more-headlines"
    market_img = ".article__figure img"  # data-srcset
    market_title = ".article__content .article__headline a"
    market_preview = ".article__subhead"

    # # src 3
    investopedia = "https://www.investopedia.com/cryptocurrency-news-5114163"
    investopedia_news = "#main_1-0"
    investopedia_indi_1 = ".comp.spotlight.mntl-block .comp.card-list__item.mntl-block"
    investopedia_indi_2 = ".comp.taxonomy-cards.mntl-block .comp.card-list__item.mntl-block"
    investopedia_img = ".card__media img"  # data-src
    investopedia_title = "a"
    investopedia_preview = "#mntl-sc-block_1-0"

    # result container
    crypto_articles = []
    preview_results = []

    # task container
    t1 = threading.Thread(target=scrap_both_belong,
                          args=(money_control, money_news, money_indi_2, money_indi_1,
                                money_title, money_img, crypto_articles, money_preview, preview_results))
    t2 = threading.Thread(target=scrap_both_belong,
                          args=(market_watch, market_news, market_indi_2, market_indi_1,
                                market_title, market_img, crypto_articles, market_preview, preview_results))
    t3 = threading.Thread(target=scrap_both_belong,
                          args=(investopedia, investopedia_news, investopedia_indi_2, investopedia_indi_1,
                                investopedia_title, investopedia_img, crypto_articles, investopedia_preview, preview_results))

    # Capture threading start time
    start_time = time.perf_counter()

    # threads working
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    # Capture threading execution time
    end_time = time.perf_counter()
    execution_time = end_time - start_time

    # [TEMPORARY]: print out the result; [FUTURE TARGET]: store in database

    count = 0
    for i in range(len(crypto_articles)):
        crypto_articles[i].append(preview_results[i])
        print(crypto_articles[i])
        count += 1

    # check if matching the number of scrapped articles
    print(count)

    # program performance check
    print('\nCheckmark: ' + str(len(crypto_articles)) + " articles in " + str(round(execution_time, 2)) + " secs (included previews)")
