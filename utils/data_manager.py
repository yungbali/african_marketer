from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime, timedelta
import json
import os
from .data_scraper import AfricanMusicDataScraper, MarketData
import glob

class DataManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.scraper = AfricanMusicDataScraper()
        self.cache: Dict[str, MarketData] = {}
        self.cache_duration = timedelta(days=1)
        
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

    async def get_market_data(self, country: str) -> Optional[MarketData]:
        """Get market data for a country, using cache if available and fresh"""
        if self._is_cache_valid(country):
            return self.cache[country]
            
        # Try to load from file first
        data = self._load_from_file(country)
        if data and self._is_data_fresh(data):
            self.cache[country] = data
            return data
            
        # If no fresh data available, scrape new data
        data = await self.scraper.scrape_market_data(country)
        if data:
            self.cache[country] = data
            self.scraper.save_to_database(data, country)
        return data

    def _is_cache_valid(self, country: str) -> bool:
        if country not in self.cache:
            return False
        return self._is_data_fresh(self.cache[country])

    def _is_data_fresh(self, data: MarketData) -> bool:
        age = datetime.now() - data.last_updated
        return age < self.cache_duration

    def _load_from_file(self, country: str) -> Optional[MarketData]:
        """Load most recent data file for country"""
        pattern = f"market_data_{country.lower()}_*.json"
        files = sorted(glob.glob(os.path.join(self.data_dir, pattern)), reverse=True)
        
        if not files:
            return None
            
        with open(files[0], 'r') as f:
            data = json.load(f)
            return MarketData(**data)

    def get_market_summary(self, countries: List[str]) -> pd.DataFrame:
        """Generate summary dataframe for multiple countries"""
        data = []
        for country in countries:
            if country in self.cache:
                market = self.cache[country]
                data.append({
                    'Country': country,
                    'Population': market.population,
                    'Streaming Revenue': market.streaming_revenue,
                    'Internet Penetration': market.internet_penetration,
                    'Smartphone Users': market.smartphone_users
                })
        return pd.DataFrame(data) 