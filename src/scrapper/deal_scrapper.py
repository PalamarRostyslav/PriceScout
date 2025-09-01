from typing import List, Dict, Self
from bs4 import BeautifulSoup
import re
import feedparser
from tqdm import tqdm
import requests
import time
from ..configs import FEEDS

class DealScraper:
    """
        A class to scrape deals from various RSS feeds.
    """
    
    category: str
    title: str
    summary: str
    url: str
    details: str
    features: str

    def __init__(self, entry: Dict[str, str]):
        """
        Populate this instance based on the provided dict
        """
        self.title = entry['title']
        self.summary = self.extract_from_html(entry['summary'])
        self.url = entry['links'][0]['href']
        
        stuff = requests.get(self.url).content
        soup = BeautifulSoup(stuff, 'html.parser')
        content = soup.find('div', class_='content-section').get_text()
        content = content.replace('\nmore', '').replace('\n', ' ')
        
        if "Features" in content:
            self.details, self.features = content.split("Features")
        else:
            self.details = content
            self.features = ""
            
    def __repr__(self):
        """
        Return a string to describe this deal
        """
        return f"<{self.title}>"

    def describe(self):
        """
        Return a longer string to describe this deal for use in calling a model
        """
        return f"Title: {self.title}\nDetails: {self.details.strip()}\nFeatures: {self.features.strip()}\nURL: {self.url}"

    def extract_from_html(self, html_snippet: str) -> str:
        """Extract relevant information from the HTML snippet using BeautifulSoup.

        Args:
            html_snippet (str): The HTML snippet to extract information from.

        Returns:
            str: The extracted information.
        """
        soup = BeautifulSoup(html_snippet, 'html.parser')
        snippet_div = soup.find('div', class_='snippet summary')
        if snippet_div:
            description = snippet_div.get_text(strip=True)
            description = BeautifulSoup(description, 'html.parser').get_text()
            description = re.sub('<[^<]+?>', '', description)
            result = description.strip()
        else:
            result = html_snippet

        return result.replace('\n', ' ')

    @classmethod
    def fetch(cls, show_progress : bool = False) -> List[Self]:
        """
        Retrieve all deals from the selected RSS feeds
        """
        deals = []
        feed_iter = tqdm(FEEDS) if show_progress else FEEDS
        for feed in feed_iter:
            parsed_feed = feedparser.parse(feed)
            for entry in parsed_feed.entries[:10]:
                deals.append(cls(entry))
                time.sleep(0.5)
        return deals
