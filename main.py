from time import time

from crawler import Crawler


if __name__ == '__main__':
    st_time = time()
    URL = str(input('Please, enter a URL: '))
    try:
        DEPTH = int(input('Please, enter depth (should be an integer number: '))
    except ValueError:
        DEPTH = 1
        print('\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('|                                             WARNING!                                              |')
        print('| Crawler does not understand entered value for DEPTH parameter.                                    |')
        print('| Using default value 1 for this run.                                                               |')
        print('| If you want to change value for DEPTH parameter, please restart a program and enter correct value.|')
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    assert len(URL) > 0, 'Please, specify a URL!'
    crawler = Crawler(url=URL, depth=DEPTH)
    crawler.crawl()
    print(f'\nCrawling is finished. Total time: {(time() - st_time):.3f}s')
