"""
데이터 처리 및 기술적 지표 계산 모듈
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List
from config import MOVING_AVERAGES, LOOKBACK_PERIODS

class DataProcessor:
    """데이터 처리 및 지표 계산 클래스"""
    
    def __init__(self, data: Dict[str, pd.DataFrame]):
        self.data = data
        self.results = {}
    
    def process_all(self) -> Dict:
        """모든 자산 데이터 처리"""
        for code, df in self.data.items():
            self.results[code] = self._process_single_asset(code, df)
        
        # 상관관계 계산
        self.results['correlations'] = self._calculate_correlations()
        
        return self.results
    
    def _process_single_asset(self, code: str, df: pd.DataFrame) -> Dict:
        """개별 자산 데이터 처리"""
        if df.empty or len(df) < 20:
            return {'error': '데이터 부족'}
        
        result = {}
        
        # 기본 정보
        result['current_price'] = float(df['close'].iloc[-1])
        result['previous_close'] = float(df['close'].iloc[-2])
        
        # 일간 변동
        result['daily_change'] = result['current_price'] - result['previous_close']
        result['daily_change_pct'] = (result['daily_change'] / result['previous_close']) * 100
        
        # 최근 7일 데이터
        result['last_7days'] = df['close'].tail(7).to_dict()
        
        # 주간 데이터
        result['weekly'] = self._calculate_period_stats(df, 'W')
        
        # 월간 데이터
        result['monthly'] = self._calculate_period_stats(df, 'M')
        
        # 이동평균선
        result['moving_averages'] = self._calculate_moving_averages(df)
        
        # 52주 최고/최저
        result['52w_high'] = float(df['close'].tail(252).max())
        result['52w_low'] = float(df['close'].tail(252).min())
        result['is_52w_high'] = result['current_price'] >= result['52w_high'] * 0.999
        result['is_52w_low'] = result['current_price'] <= result['52w_low'] * 1.001
        
        # 골든크로스/데드크로스 감지
        result['cross_signals'] = self._detect_cross_signals(df)
        
        return result
    
    def _calculate_period_stats(self, df: pd.DataFrame, freq: str) -> Dict:
        """기간별 통계 계산"""
        # 주간/월간 리샘플링
        resampled = df['close'].resample(freq).last().dropna()
        
        if len(resampled) < 2:
            return {}
        
        stats = {
            'current_period_avg': float(resampled.iloc[-1]),
            'last_period_avg': float(resampled.iloc[-2]) if len(resampled) >= 2 else None,
            'last_2_period_avg': float(resampled.iloc[-3]) if len(resampled) >= 3 else None,
            'last_3month_avg': float(resampled.tail(3).mean()) if len(resampled) >= 3 else None,
            'last_6month_avg': float(resampled.tail(6).mean()) if len(resampled) >= 6 else None,
            'last_12month_avg': float(resampled.tail(12).mean()) if len(resampled) >= 12 else None,
        }
        
        return stats
    
    def _calculate_moving_averages(self, df: pd.DataFrame) -> Dict:
        """이동평균선 계산"""
        ma_values = {}
        current_price = float(df['close'].iloc[-1])
        
        for period in MOVING_AVERAGES:
            if len(df) >= period:
                ma = float(df['close'].tail(period).mean())
                ma_values[f'MA{period}'] = {
                    'value': ma,
                    'divergence': ((current_price - ma) / ma) * 100,
                    'position': 'above' if current_price > ma else 'below'
                }
        
        return ma_values
    
    def _detect_cross_signals(self, df: pd.DataFrame) -> Dict:
        """크로스 신호 감지"""
        signals = {}
        
        if len(df) < 20:
            return signals
        
        # MA5 vs MA20
        ma5 = df['close'].rolling(5).mean()
        ma20 = df['close'].rolling(20).mean()
        
        # 골든크로스: MA5가 MA20을 상향 돌파
        if len(ma5) >= 2 and len(ma20) >= 2:
            if ma5.iloc[-2] <= ma20.iloc[-2] and ma5.iloc[-1] > ma20.iloc[-1]:
                signals['golden_cross_5_20'] = True
            # 데드크로스: MA5가 MA20을 하향 돌파
            elif ma5.iloc[-2] >= ma20.iloc[-2] and ma5.iloc[-1] < ma20.iloc[-1]:
                signals['dead_cross_5_20'] = True
        
        # 정배열/역배열 확인
        if len(df) >= 60:
            ma5_val = ma5.iloc[-1]
            ma20_val = ma20.iloc[-1]
            ma60_val = df['close'].rolling(60).mean().iloc[-1]
            
            if ma5_val > ma20_val > ma60_val:
                signals['bullish_alignment'] = True
            elif ma5_val < ma20_val < ma60_val:
                signals['bearish_alignment'] = True
        
        return signals
    
    def _calculate_correlations(self) -> Dict:
        """자산 간 상관관계 계산"""
        correlations = {}
        
        # 최근 60일 데이터로 상관관계 계산
        price_data = {}
        for code, df in self.data.items():
            if len(df) >= 60:
                price_data[code] = df['close'].tail(60).pct_change().dropna()
        
        # 모든 쌍의 상관관계 계산
        codes = list(price_data.keys())
        for i in range(len(codes)):
            for j in range(i+1, len(codes)):
                code1, code2 = codes[i], codes[j]
                if len(price_data[code1]) > 0 and len(price_data[code2]) > 0:
                    common_idx = price_data[code1].index.intersection(price_data[code2].index)
                    if len(common_idx) > 20:
                        corr = price_data[code1].loc[common_idx].corr(
                            price_data[code2].loc[common_idx]
                        )
                        correlations[f"{code1}_{code2}"] = float(corr)
        
        return correlations
