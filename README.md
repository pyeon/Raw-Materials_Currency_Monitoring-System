# 📊 원자재/통화 모니터링 시스템

GitHub Actions를 활용한 자동화된 원자재 및 통화 시세 모니터링 시스템

## 🎯 주요 기능

- **자동 데이터 수집**: 매일 오전 9시(KST) 자동 실행
- **다층 알림 시스템**: 일반/주의/긴급 3단계 알림
- **종합 분석**: 이동평균, 크로스 신호, 상관관계 분석
- **상세 리포트**: 엑셀 파일로 자동 생성 및 텔레그램 전송

## 📦 모니터링 대상

### 원자재
- 금 (Gold)
- 은 (Silver)
- 구리 (Copper)
- 원유 (WTI Crude Oil)

### 통화
- 달러/원 (USD/KRW)
- 달러/엔 (USD/JPY)
- 유로/달러 (EUR/USD)

## ⚙️ 설정 방법

### 1. Repository Secrets 설정

GitHub 저장소 Settings > Secrets and variables > Actions에서 다음 변수 추가:
```
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### 2. 텔레그램 봇 생성

1. [@BotFather](https://t.me/botfather)에게 `/newbot` 명령
2. 봇 이름 및 username 설정
3. 받은 토큰을 `TELEGRAM_BOT_TOKEN`에 입력

### 3. Chat ID 확인

1. 생성한 봇과 대화 시작
2. https://api.telegram.org/bot{BOT_TOKEN}/getUpdates 접속
3. `chat.id` 값을 `TELEGRAM_CHAT_ID`에 입력

### 4. 저장소에 Push
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

## 🚀 수동 실행

GitHub Actions 탭에서 `Commodity & Currency Daily Monitor` 워크플로우 선택 후 `Run workflow` 클릭

## 📋 알림 조건

### Level 1: 일일 리포트 (무조건 발송)
- 전체 자산 현황 요약
- 조용한 알림 (진동 없음)

### Level 2: 주의 알림
- 일간 변동률 ±2% 이상
- MA 골든크로스/데드크로스

### Level 3: 긴급 알림
- 일간 변동률 ±3% 이상
- 52주 최고/최저가 경신
- 정배열/역배열 진입
- 상관관계 이상 패턴

## 📊 엑셀 리포트 구성

1. **종합요약**: 전체 자산 현황 한눈에
2. **일자별상세**: 최근 7일 일자별 시세
3. **주간추이**: 주별 평균 및 변동률
4. **월간추이**: 월별 평균 및 장기 추세
5. **기술지표**: 이동평균, 크로스 신호
6. **상관관계**: 자산 간 상관계수 분석

## 🔧 커스터마이징

`src/config.py`에서 다음 설정 변경 가능:

- 모니터링 대상 추가/제거
- 알림 임계값 조정
- 이동평균선 기간 변경
- 데이터 수집 주기 조정

### 자산 추가 예시
```python
# src/config.py

ASSETS = {
    'commodities': {
        'PLATINUM': {
            'name': '백금',
            'spot_ticker': 'PL=F',
            'unit': 'oz',
            'icon': '⚪',
            'enabled': True  # 👈 True로 변경하면 활성화
        },
    }
}
```

자세한 자산 관리 가이드는 [ASSET_GUIDE.md](ASSET_GUIDE.md) 참조

## 📝 라이선스

MIT License

## 🤝 기여

이슈 및 PR 환영합니다!

## 📧 문의

이슈 탭에 질문을 남겨주세요.
