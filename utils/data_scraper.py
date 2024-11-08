import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import Dict, List, Optional
import logging
from datetime import datetime
import json
import aiohttp
import asyncio
from dataclasses import dataclass
from fake_useragent import UserAgent

@dataclass
class StreamingPlatformData:
    name: str
    market_share: float
    monthly_active_users: int
    local: bool
    supported_countries: List[str]

@dataclass
class MarketData:
    last_updated: datetime
    population: int
    gdp_per_capita: float
    internet_penetration: float
    smartphone_users: int
    streaming_revenue: float
    digital_payment_penetration: float
    platforms: List[StreamingPlatformData]
    genre_popularity: Dict[str, float]
    languages: List[str]
    artist_demographics: Dict[str, float]

class AfricanMusicDataScraper:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ua = UserAgent()
        self.base_urls = {
            'ifpi': 'https://www.ifpi.org/resources/',
            'worldbank': 'https://data.worldbank.org/country/',
            'gsma': 'https://www.gsma.com/mobileeconomy/africa/',
            'statista': 'https://www.statista.com/markets/422/topic/494/music/#overview'
        }
        
    async def _fetch_page(self, url: str) -> Optional[str]:
        headers = {'User-Agent': self.ua.random}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        return await response.text()
                    self.logger.error(f"Failed to fetch {url}: Status {response.status}")
                    return None
        except Exception as e:
            self.logger.error(f"Error fetching {url}: {str(e)}")
            return None

    async def scrape_market_data(self, country: str) -> Optional[MarketData]:
        tasks = []
        for source, url in self.base_urls.items():
            tasks.append(self._fetch_page(f"{url}{country.lower()}"))
        
        results = await asyncio.gather(*tasks)
        
        if not any(results):
            return None
            
        return self._parse_market_data(country, results)

    def _parse_market_data(self, country: str, raw_data: List[str]) -> MarketData:
        # Implementation of parsing logic for each data source
        # This is a simplified version - real implementation would be more complex
        market_data = {
            'last_updated': datetime.now(),
            'population': self._extract_population(raw_data[1]),  # WorldBank data
            'gdp_per_capita': self._extract_gdp(raw_data[1]),
            'internet_penetration': self._extract_internet_stats(raw_data[2]),  # GSMA data
            'smartphone_users': self._extract_smartphone_stats(raw_data[2]),
            'streaming_revenue': self._extract_streaming_revenue(raw_data[0]),  # IFPI data
            'digital_payment_penetration': self._extract_payment_stats(raw_data[2]),
            'platforms': self._extract_platform_data(raw_data[3]),  # Statista data
            'genre_popularity': self._extract_genre_data(raw_data[3]),
            'languages': self._get_country_languages(country),
            'artist_demographics': self._extract_artist_data(raw_data[3])
        }
        
        return MarketData(**market_data)

    def save_to_database(self, data: MarketData, country: str):
        """Save scraped data to local JSON database"""
        filename = f"data/market_data_{country.lower()}_{data.last_updated.strftime('%Y%m%d')}.json"
        with open(filename, 'w') as f:
            json.dump(data.__dict__, f, default=str)