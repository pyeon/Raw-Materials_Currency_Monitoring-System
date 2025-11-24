"""
원자재/통화 데이터 수집 모듈
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Optional
import time
from config import get_enabled_assets, LOOKBACK_PERIODS, DATA_DIR
import os

class DataCollector:
    """데이터 수집 클래스"""
    
    def __init__(self):
        self.lookback_days = LOOKBACK_PERIODS['ma_calculation'] + 30
        self.assets = get_enabled_assets()
        
    def collect_all_data(self) -> Dict[str, pd.DataFrame]:
        """모든 자산 데이터 수집"""
        all_data = {}
        
        # 원자재 데이터 수집
        for code, info in self.assets.get('commodities', {}).items():
            print(f"📊 {info['name']} 데이터 수집 중...")
            ticker = info.get('spot_ticker') or info.get('ticker')
            data = self._fetch_yfinance_data(ticker)
            if data is not None:
                all_data[code] = data
                self._save_to_csv(code, data)
            time.sleep(1)
        
        # 통화 데이터 수집
        for code, info in self.assets.get('currencies', {}).items():
            print(f"💱 {info['name']} 데이터 수집 중...")
            data = self._fetch_yfinance_data(info['ticker'])
            if data is not None:
                all_data[code] = data
                self._save_to_csv(code, data)
            time.sleep(1)
        
        # 암호화폐 데이터 수집 (있다면)
        for code, info in self.assets.get('cryptocurrencies', {}).items():
            print(f"₿ {info['name']} 데이터 수집 중...")
            data = self._fetch_yfinance_data(info['ticker'])
            if data is not None:
                all_data[code] = data
                self._save_to_csv(code, data)
            time.sleep(1)
        
        return all_data
    
    def _fetch_yfinance_data(self, ticker: str) -> Optional[pd.DataFrame]:
        """Yahoo Finance에서 데이터 가져오기"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=self.lookback_days)
            
            data = yf.download(
                ticker,
                start=start_date,
                end=end_date,
                progress=False
            )
            
            if data.empty:
                print(f"⚠️  {ticker} 데이터 없음")
                return None
            
            # 컬럼명 정리
            data = data.rename(columns={
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume'
            })
            
            return data[['close', 'open', 'high', 'low', 'volume']]
            
        except Exception as e:
            print(f"❌ {ticker} 수집 실패: {e}")
            return None
    
    def _save_to_csv(self, code: str, data: pd.DataFrame):
        """CSV 파일로 저장"""
        os.makedirs(DATA_DIR, exist_ok=True)
        filepath = f"{DATA_DIR}/{code}_history.csv"
        data.to_csv(filepath)
        print(f"✅ {code} 데이터 저장: {filepath}")
