from src.agents.agent import Agent
from src.scrapper.deal_scrapper import DealScraper

deals = DealScraper.fetch(show_progress=True)
len(deals)