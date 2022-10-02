import os
import requests
import time
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import Optional


@dataclass
class Link:
    """
    Class for logging appropriate links.
    """
    id: int
    html: Optional[BeautifulSoup]
    url: str


class Crawler:
    """
    Class for crawling.
    """
    depth: int
    found_urls: dict
    links_storage: list
    start_url: str
    storage_path: Optional[str] = None

    def __init__(self, url: str, depth: int):
        """
        Method for Crawler initialization.

        Parameters
        ----------
        url: str
            Entered (starting) url

        depth: int
            Entered depth for crawling
        """
        self.start_url = url
        self.depth = depth
        self.found_urls = {i: [] for i in range(self.depth)}
        self.links_storage = []

    def crawl(self):
        """
        Main method of class for crawling.
        """
        link_id = 0
        for i in range(self.depth):
            if i == 0:
                self.crawl_start_url(link_id)
                link_id += 1
            elif i in self.found_urls:
                self.crawl_url(i, link_id)
                link_id = len(self.links_storage)
        self.store_results()

    def crawl_start_url(self, link_id: int) -> Optional:
        """
        Method for crawling of starting url (made for decreasing complexity of main method).

        Parameters
        ----------
        link_id: int
            Id of url for crawling (always 0 for starting url)

        Returns
        -------
        None if something went wrong with parsing of starting url
        """
        st_time = time.time()
        self.found_urls[0].append(self.start_url)
        print('\nWorking with given URL.')
        html = self.crawl_link(self.start_url, 0)
        if html is None:
            return
        self.links_storage.append(Link(link_id, html, self.start_url))
        self.found_urls[1] = set(self.found_urls[1])
        print(f'Finished working with given URL. Found {len(self.found_urls[1])} URLs on it. Time for crawling'
              f'of entered URL: {(time.time() - st_time):.3f}s')

    def crawl_url(self, depth: int, link_id: int):
        """
        Method for crawling of url (made for decreasing complexity of main method).

        Parameters
        ----------
        depth: int
            Depth level of urls for parsing

        link_id: int
            Id of url for crawling
        """
        for url in self.found_urls[depth]:
            if self.checker(url, depth):
                continue
            st_time = time.time()
            html = self.crawl_link(url, depth)
            if html is None:
                continue
            self.links_storage.append(Link(link_id, html, url))
            link_id += 1
            print(f'\nFinished working with URL {url}. Time for crawling it: {(time.time() - st_time):.3f}s')
        if depth != self.depth - 1:
            self.found_urls[depth + 1] = set(self.found_urls[depth + 1])

    @staticmethod
    def get_page_by_url(url: str) -> Optional[requests.Response]:
        """
        Method for parsing url.

        Parameters
        ----------
        url: str
            Url for parsing

        Returns
        -------
        None if something went wrong with parsing url, else parsed url
        """
        if url is None or not url.startswith('http'):
            return None
        try:
            time.sleep(1.5)
            page = requests.get(url)
            return page
        except requests.exceptions.MissingSchema:
            if not url.startswith('http'):
                return None
            print(f'\nFound invalid URL: {url}. It is excluded from the list. Please, check it by yourself!')
            return None
        except requests.exceptions.ConnectionError:
            print(f'\nFound invalid URL: {url}. Something wrong with connection :(')
            return None
        except requests.exceptions.InvalidSchema:
            print(f'\nFound invalid URL: {url}. Something wrong with connection :(')
            return None

    def crawl_link(self, url: str, depth: int) -> Optional[BeautifulSoup]:
        """
        Method for extracting all urls from given url.

        Parameters
        ----------
        url: str
            Url for searching for other urls

        depth: int
            Depth level of given url

        Returns
        -------
        None if something went wrong with parsing url, else parsed url
        """
        page = self.get_page_by_url(url)
        if page is None:
            return None
        soup = BeautifulSoup(page.text, 'html.parser')
        for link in soup.find_all('a'):
            if depth + 1 in self.found_urls:
                self.found_urls[depth + 1].append(link.get('href'))
            else:
                self.found_urls[depth + 1] = [link.get('href')]
        return soup

    def checker(self, url: str, depth: int) -> bool:
        """
        Method for checking if given url on previous levels of depth.

        Parameters
        ----------
        url: str
            Url for checking

        depth: int
            Depth level of given url

        Returns
        -------
        True if url is already parsed
        """
        for i in range(depth):
            if url in self.found_urls[i]:
                return True
        return False

    def store_results(self):
        """
        Method for saving results as given in task.
        """
        print('\nStarted storing results! Almost done :)')
        if self.storage_path is None:
            self.storage_path = os.getcwd()
        try:
            os.mkdir(self.storage_path + '/data')
            self.storage_path += '/data'
        except FileExistsError:
            self.storage_path = self.storage_path + '/data'
        with open(self.storage_path[:-4] + 'urls.txt', 'w') as f:
            for link in self.links_storage:
                f.write(str(link.id) + ' ' + str(link.url) + '\n')
                with open(self.storage_path + f'/{link.id}.html', 'w') as content:
                    content.write(link.html.text)
