"""
원자재/통화 모니터링 시스템 설정
"""
import os
from datetime import datetime

# ==================== 기본 설정 ====================
TIMEZONE = 'Asia/Seoul'
DATA_DIR = 'data'
REPORT_DIR = 'reports'

# ==================== 모니터링 대상 ====================
# 👉 여기서 자산을 쉽게 추가/제거할 수 있습니다!

ASSETS = {
    'commodities': {
        # 귀금속
        'GOLD': {
            'name': '금',
            'spot_ticker': 'GC=F',      # 금 선물
            'unit': 'oz',
            'icon': '💰',
            'enabled': True
        },
        'SILVER': {
            'name': '은',
            'spot_ticker': 'SI=F',      # 은 선물
            'unit': 'oz',
            'icon': '💎',
            'enabled': True
        },
        'PLATINUM': {
            'name': '백금',
            'spot_ticker': 'PL=F',      # 백금 선물
            'unit': 'oz',
            'icon': '⚪',
            'enabled': False
        },
        'PALLADIUM': {
            'name': '팔라듐',
            'spot_ticker': 'PA=F',      # 팔라듐 선물
            'unit': 'oz',
            'icon': '⚫',
            'enabled': False
        },
        
        # 비철금속
        'COPPER': {
            'name': '구리',
            'spot_ticker': 'HG=F',      # 구리 선물
            'unit': 'lb',
            'icon': '🟫',
            'enabled': True
        },
        'ALUMINUM': {
            'name': '알루미늄',
            'spot_ticker': 'ALI=F',     # 알루미늄 선물
            'unit': 'MT',
            'icon': '⚙️',
            'enabled': False
        },
        'NICKEL': {
            'name': '니켈',
            'spot_ticker': 'NKL.L',     # 니켈 (런던)
            'unit': 'MT',
            'icon': '🔩',
            'enabled': False
        },
        
        # 에너지
        'CRUDE_OIL': {
            'name': '원유(WTI)',
            'spot_ticker': 'CL=F',      # WTI 원유 선물
            'unit': 'bbl',
            'icon': '🛢️',
            'enabled': True
        },
        'BRENT_OIL': {
            'name': '원유(브렌트)',
            'spot_ticker': 'BZ=F',      # 브렌트 원유 선물
            'unit': 'bbl',
            'icon': '🛢️',
            'enabled': False
        },
        'NATURAL_GAS': {
            'name': '천연가스',
            'spot_ticker': 'NG=F',      # 천연가스 선물
            'unit': 'MMBtu',
            'icon': '🔥',
            'enabled': False
        },
        
        # 농산물
        'WHEAT': {
            'name': '밀',
            'spot_ticker': 'ZW=F',      # 밀 선물
            'unit': 'bu',
            'icon': '🌾',
            'enabled': False
        },
        'CORN': {
            'name': '옥수수',
            'spot_ticker': 'ZC=F',      # 옥수수 선물
            'unit': 'bu',
            'icon': '🌽',
            'enabled': False
        },
        'SOYBEAN': {
            'name': '대두',
            'spot_ticker': 'ZS=F',      # 대두 선물
            'unit': 'bu',
            'icon': '🫘',
            'enabled': False
        },
        
        # 축산물
        'LEAN_HOGS': {
            'name': '돼지고기',
            'spot_ticker': 'HE=F',      # 돈육 선물
            'unit': 'lb',
            'icon': '🥓',
            'enabled': False
        },
        'LIVE_CATTLE': {
            'name': '소고기',
            'spot_ticker': 'LE=F',      # 육우 선물
            'unit': 'lb',
            'icon': '🥩',
            'enabled': False
        },
    },
    
    'currencies': {
        # 아시아
        'USD_KRW': {
            'name': '달러/원',
            'ticker': 'KRW=X',
            'icon': '💵',
            'enabled': True
        },
        'USD_JPY': {
            'name': '달러/엔',
            'ticker': 'JPY=X',
            'icon': '💴',
            'enabled': True
        },
        'USD_CNY': {
            'name': '달러/위안',
            'ticker': 'CNY=X',
            'icon': '💴',
            'enabled': False
        },
        
        # 유럽
        'EUR_USD': {
            'name': '유로/달러',
            'ticker': 'EURUSD=X',
            'icon': '💶',
            'enabled': True
        },
        'GBP_USD': {
            'name': '파운드/달러',
            'ticker': 'GBPUSD=X',
            'icon': '💷',
            'enabled': False
        },
        
        # 기타
        'AUD_USD': {
            'name': '호주달러/달러',
            'ticker': 'AUDUSD=X',
            'icon': '🇦🇺',
            'enabled': False
        },
        'USD_CAD': {
            'name': '달러/캐나다달러',
            'ticker': 'CAD=X',
            'icon': '🇨🇦',
            'enabled': False
        },
    },
    
    # 새로운 카테고리 추가 가능
    'cryptocurrencies': {
        'BTC': {
            'name': '비트코인',
            'ticker': 'BTC-USD',
            'icon': '₿',
            'enabled': False
        },
        'ETH': {
            'name': '이더리움',
            'ticker': 'ETH-USD',
            'icon': '♦️',
            'enabled': False
        },
    }
}

# 활성화된 자산만 필터링하는 헬퍼 함수
def get_enabled_assets():
    """활성화된 자산만 반환"""
    enabled = {}
    for category, assets in ASSETS.items():
        enabled[category] = {
            code: info for code, info in assets.items() 
            if info.get('enabled', True)
        }
    return enabled

# ==================== Yahoo Finance 티커 참조 가이드 ====================
# 
# 선물 계약 (Futures):
# - 금 (Gold): GC=F
# - 은 (Silver): SI=F
# - 구리 (Copper): HG=F
# - 백금 (Platinum): PL=F
# - 팔라듐 (Palladium): PA=F
# - 원유 WTI (Crude Oil WTI): CL=F
# - 원유 브렌트 (Brent Crude): BZ=F
# - 천연가스 (Natural Gas): NG=F
# - 밀 (Wheat): ZW=F
# - 옥수수 (Corn): ZC=F
# - 대두 (Soybeans): ZS=F
#
# 통화 (Forex):
# - 달러/원: KRW=X
# - 달러/엔: JPY=X
# - 유로/달러: EURUSD=X
# - 파운드/달러: GBPUSD=X
#
# 💡 더 많은 티커는 Yahoo Finance에서 검색:
# https://finance.yahoo.com/commodities
# https://finance.yahoo.com/currencies

# ==================== 알림 조건 ====================
ALERT_THRESHOLDS = {
    # Level 2: 주의 알림
    'warning': {
        'daily_change': 2.0,      # 일간 변동률 ±2%
        'weekly_change': 5.0,     # 주간 변동률 ±5%
    },
    # Level 3: 긴급 알림
    'emergency': {
        'daily_change': 3.0,      # 일간 변동률 ±3%
        'weekly_change': 7.0,     # 주간 변동률 ±7%
        '52w_extreme': True,      # 52주 최고/최저 경신
    }
}

# ==================== 이동평균선 설정 ====================
MOVING_AVERAGES = [5, 20, 60, 120]

# ==================== 상관관계 설정 ====================
CORRELATION_PATTERNS = {
    'USD_KRW_GOLD': {
        'assets': ['USD_KRW', 'GOLD'],
        'expected': 'negative',
        'threshold': -0.3,
        'alert_message': '달러↑인데 금도↑ (비정상)'
    },
    'GOLD_SILVER': {
        'assets': ['GOLD', 'SILVER'],
        'expected': 'positive',
        'threshold': 0.5,
        'alert_message': '금↑인데 은↓ (비정상)'
    },
}

# ==================== 데이터 기간 설정 ====================
LOOKBACK_PERIODS = {
    'daily': 7,
    'weekly': 12,
    'monthly': 24,
    'ma_calculation': 250
}

# ==================== API 설정 ====================
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', '')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

# ==================== 엑셀 리포트 설정 ====================
EXCEL_CONFIG = {
    'daily_update': True,
    'weekly_summary': True,
    'monthly_summary': True,
}
