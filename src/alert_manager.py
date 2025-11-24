"""
알림 조건 판단 및 관리 모듈
"""
from typing import Dict, List
from config import ALERT_THRESHOLDS, CORRELATION_PATTERNS, get_enabled_assets

class AlertManager:
    """알림 관리 클래스"""
    
    def __init__(self, processed_data: Dict):
        self.data = processed_data
        self.assets = get_enabled_assets()
        self.alerts = {
            'level1': [],
            'level2': [],
            'level3': []
        }
    
    def generate_alerts(self) -> Dict[str, List]:
        """모든 알림 생성"""
        # Level 1: 일반 리포트 (모든 자산)
        self._generate_daily_report()
        
        # Level 2: 주의 알림
        self._check_warning_conditions()
        
        # Level 3: 긴급 알림
        self._check_emergency_conditions()
        
        # 상관관계 이상 감지
        self._check_correlation_anomalies()
        
        return self.alerts
    
    def _generate_daily_report(self):
        """일일 리포트 생성 (Level 1)"""
        report_lines = []
        
        for category, assets in self.assets.items():
            for code, info in assets.items():
                if code not in self.data or 'error' in self.data[code]:
                    continue
                
                d = self.data[code]
                icon = info['icon']
                name = info['name']
                price = d['current_price']
                change_pct = d['daily_change_pct']
                
                # 주간/월간 추세
                weekly_info = ""
                if 'weekly' in d and d['weekly']:
                    weekly = d['weekly']
                    if 'last_period_avg' in weekly and weekly['last_period_avg']:
                        weekly_change = ((d['current_price'] - weekly['last_period_avg']) / 
                                       weekly['last_period_avg'] * 100)
                        weekly_info = f"주간 {weekly_change:+.1f}%"
                
                # 이동평균 정보
                ma_info = ""
                if 'moving_averages' in d:
                    ma = d['moving_averages']
                    if 'MA5' in ma and 'MA20' in ma and 'MA60' in ma:
                        if (ma['MA5']['position'] == 'above' and 
                            ma['MA20']['position'] == 'above' and 
                            ma['MA60']['position'] == 'above'):
                            ma_info = "📈"
                        elif (ma['MA5']['position'] == 'below' and 
                              ma['MA20']['position'] == 'below' and 
                              ma['MA60']['position'] == 'below'):
                            ma_info = "📉"
                
                line = f"{icon} {name}: {price:,.2f} ({change_pct:+.2f}%)"
                if weekly_info:
                    line += f" | {weekly_info}"
                if ma_info:
                    line += f" {ma_info}"
                
                report_lines.append(line)
        
        self.alerts['level1'] = report_lines
    
    def _check_warning_conditions(self):
        """주의 조건 체크 (Level 2)"""
        warnings = []
        
        for category, assets in self.assets.items():
            for code, info in assets.items():
                if code not in self.data or 'error' in self.data[code]:
                    continue
                
                d = self.data[code]
                name = info['name']
                
                # 일간 변동률 체크
                if abs(d['daily_change_pct']) >= ALERT_THRESHOLDS['warning']['daily_change']:
                    warnings.append(
                        f"📊 {name} 일간 {d['daily_change_pct']:+.2f}%"
                    )
                
                # 크로스 신호
                if 'cross_signals' in d:
                    signals = d['cross_signals']
                    if signals.get('golden_cross_5_20'):
                        warnings.append(f"⚡ {name} MA5↗MA20 골든크로스")
                    if signals.get('dead_cross_5_20'):
                        warnings.append(f"⚡ {name} MA5↘MA20 데드크로스")
        
        self.alerts['level2'] = warnings
    
    def _check_emergency_conditions(self):
        """긴급 조건 체크 (Level 3)"""
        emergencies = []
        
        for category, assets in self.assets.items():
            for code, info in assets.items():
                if code not in self.data or 'error' in self.data[code]:
                    continue
                
                d = self.data[code]
                name = info['name']
                
                # 급등락
                if abs(d['daily_change_pct']) >= ALERT_THRESHOLDS['emergency']['daily_change']:
                    emoji = "🚀" if d['daily_change_pct'] > 0 else "💥"
                    emergencies.append(
                        f"{emoji} {name} 급{'등' if d['daily_change_pct'] > 0 else '락'} "
                        f"{d['daily_change_pct']:+.2f}%"
                    )
                
                # 52주 최고/최저 경신
                if d.get('is_52w_high'):
                    emergencies.append(f"🔔 {name} 52주 최고가 경신 ({d['current_price']:,.2f})")
                if d.get('is_52w_low'):
                    emergencies.append(f"🔔 {name} 52주 최저가 경신 ({d['current_price']:,.2f})")
                
                # 정배열/역배열
                if 'cross_signals' in d:
                    signals = d['cross_signals']
                    if signals.get('bullish_alignment'):
                        emergencies.append(f"📈 {name} 정배열 진입 (MA5>MA20>MA60)")
                    if signals.get('bearish_alignment'):
                        emergencies.append(f"📉 {name} 역배열 진입 (MA5<MA20<MA60)")
        
        self.alerts['level3'] = emergencies
    
    def _check_correlation_anomalies(self):
        """상관관계 이상 감지"""
        if 'correlations' not in self.data:
            return
        
        correlations = self.data['correlations']
        anomalies = []
        
        for pattern_name, pattern_info in CORRELATION_PATTERNS.items():
            assets = pattern_info['assets']
            expected = pattern_info['expected']
            threshold = pattern_info['threshold']
            
            # 상관계수 찾기
            pair_key = f"{assets[0]}_{assets[1]}"
            reverse_key = f"{assets[1]}_{assets[0]}"
            
            corr = correlations.get(pair_key) or correlations.get(reverse_key)
            
            if corr is None:
                continue
            
            # 이상 패턴 감지
            is_anomaly = False
            if expected == 'negative' and corr > -threshold:
                is_anomaly = True
            elif expected == 'positive' and corr < threshold:
                is_anomaly = True
            
            if is_anomaly:
                # 실제 가격 변동 확인
                changes = []
                for asset in assets:
                    if asset in self.data and 'daily_change_pct' in self.data[asset]:
                        changes.append(self.data[asset]['daily_change_pct'])
                
                if len(changes) == 2:
                    asset1_name = self._get_asset_name(assets[0])
                    asset2_name = self._get_asset_name(assets[1])
                    anomalies.append(
                        f"⚠️ 비정상 패턴: {asset1_name} {changes[0]:+.1f}% "
                        f"& {asset2_name} {changes[1]:+.1f}% (상관계수: {corr:.2f})"
                    )
        
        if anomalies:
            self.alerts['level3'].extend(anomalies)
    
    def _get_asset_name(self, code: str) -> str:
        """자산 코드로 이름 찾기"""
        for category, assets in self.assets.items():
            if code in assets:
                return assets[code]['name']
        return code
