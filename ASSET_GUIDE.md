# 📚 자산 추가/관리 가이드

## 🚀 빠른 시작

자산을 추가하려면 `src/config.py`의 `ASSETS` 딕셔너리만 수정하면 됩니다!

## 📝 추가 방법

### 1. 원자재 추가
```python
'YOUR_ASSET_CODE': {
    'name': '자산명 (한글)',
    'spot_ticker': 'TICKER=F',  # Yahoo Finance 티커
    'unit': 'oz',               # 단위
    'icon': '💰',               # 이모지
    'enabled': True             # 활성화 여부
}
```

### 2. 통화 추가
```python
'YOUR_CURRENCY': {
    'name': '통화명',
    'ticker': 'XXX=X',  # Yahoo Finance 티커
    'icon': '💵',
    'enabled': True
}
```

## 🔍 Yahoo Finance 티커 찾기

1. https://finance.yahoo.com 방문
2. 원하는 자산 검색
3. URL 또는 페이지에서 티커 확인

### 티커 형식

- **선물**: `SYMBOL=F` (예: GC=F, CL=F)
- **통화**: `XXX=X` (예: KRW=X, JPY=X)
- **암호화폐**: `SYMBOL-USD` (예: BTC-USD, ETH-USD)

## 💡 자주 묻는 질문

**Q: 티커를 어떻게 찾나요?**
A: Yahoo Finance에서 검색하거나 아래 참조:
- 원자재: https://finance.yahoo.com/commodities
- 통화: https://finance.yahoo.com/currencies

**Q: 데이터가 안 나와요**
A: Yahoo Finance에서 해당 티커가 제공되는지 확인하세요.

**Q: 새 카테고리를 추가할 수 있나요?**
A: 네! `ASSETS`에 새 키를 추가하고 `data_collector.py`에 해당 카테고리 처리 로직을 추가하세요.

## 📋 인기 자산 티커 모음

### 귀금속
- 금: GC=F
- 은: SI=F
- 백금: PL=F
- 팔라듐: PA=F

### 에너지
- WTI 원유: CL=F
- 브렌트 원유: BZ=F
- 천연가스: NG=F

### 농산물
- 밀: ZW=F
- 옥수수: ZC=F
- 대두: ZS=F
- 커피: KC=F
- 설탕: SB=F

### 비철금속
- 구리: HG=F
- 알루미늄: ALI=F

### 통화
- 달러/원: KRW=X
- 달러/엔: JPY=X
- 유로/달러: EURUSD=X
- 파운드/달러: GBPUSD=X

### 암호화폐
- 비트코인: BTC-USD
- 이더리움: ETH-USD

## 🎯 추가 예제

### 예제 1: 백금 모니터링 시작
```python
# config.py에서
'PLATINUM': {
    'name': '백금',
    'spot_ticker': 'PL=F',
    'unit': 'oz',
    'icon': '⚪',
    'enabled': True  # 👈 False를 True로 변경
},
```

저장 후 다음 실행 시 자동으로 백금 데이터가 수집됩니다!

### 예제 2: 비트코인 추가
```python
# config.py의 cryptocurrencies 섹션에서
'BTC': {
    'name': '비트코인',
    'ticker': 'BTC-USD',
    'icon': '₿',
    'enabled': True  # 👈 활성화
},
```

### 예제 3: 새 자산 추가 (커피)
```python
# config.py의 commodities 섹션에 추가
'COFFEE': {
    'name': '커피',
    'spot_ticker': 'KC=F',
    'unit': 'lb',
    'icon': '☕',
    'enabled': True
},
```

## ⚙️ 고급 설정

### 알림 임계값 변경
```python
# config.py
ALERT_THRESHOLDS = {
    'warning': {
        'daily_change': 1.5,  # 👈 2.0에서 1.5로 변경 (더 민감하게)
    },
    'emergency': {
        'daily_change': 2.5,  # 👈 3.0에서 2.5로 변경
    }
}
```

### 이동평균선 기간 변경
```python
# config.py
MOVING_AVERAGES = [5, 20, 60, 120, 200]  # 👈 MA200 추가
```

### 상관관계 패턴 추가
```python
# config.py
CORRELATION_PATTERNS = {
    'CRUDE_OIL_COPPER': {
        'assets': ['CRUDE_OIL', 'COPPER'],
        'expected': 'positive',  # 정상관 예상
        'threshold': 0.4,
        'alert_message': '원유↑인데 구리↓ (비정상)'
    },
}
```

## 🔧 문제 해결

### 데이터가 수집되지 않을 때

1. Yahoo Finance에서 티커 확인
2. `enabled: True`로 설정했는지 확인
3. GitHub Actions 로그 확인

### 알림이 오지 않을 때

1. Telegram Bot Token과 Chat ID 확인
2. GitHub Secrets 설정 확인
3. 봇과 대화를 시작했는지 확인

## 📞 도움말

더 많은 정보가 필요하면 이슈를 생성해주세요!
