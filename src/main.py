"""
원자재/통화 모니터링 시스템 - 메인 실행 파일
"""
import sys
from datetime import datetime
from data_collector import DataCollector
from data_processor import DataProcessor
from alert_manager import AlertManager
from telegram_notifier import TelegramNotifier
from excel_reporter import ExcelReporter

def main():
    """메인 실행 함수"""
    print("=" * 50)
    print("🚀 원자재/통화 모니터링 시스템 시작")
    print(f"⏰ 실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    try:
        # 1. 데이터 수집
        print("\n📥 Step 1: 데이터 수집 중...")
        collector = DataCollector()
        raw_data = collector.collect_all_data()
        
        if not raw_data:
            print("❌ 수집된 데이터가 없습니다.")
            return False
        
        print(f"✅ {len(raw_data)}개 자산 데이터 수집 완료")
        
        # 2. 데이터 처리
        print("\n📊 Step 2: 데이터 처리 및 지표 계산 중...")
        processor = DataProcessor(raw_data)
        processed_data = processor.process_all()
        print("✅ 데이터 처리 완료")
        
        # 3. 알림 생성
        print("\n🔔 Step 3: 알림 조건 분석 중...")
        alert_manager = AlertManager(processed_data)
        alerts = alert_manager.generate_alerts()
        
        print(f"   - Level 1 (일반): {len(alerts['level1'])}개")
        print(f"   - Level 2 (주의): {len(alerts['level2'])}개")
        print(f"   - Level 3 (긴급): {len(alerts['level3'])}개")
        
        # 4. 엑셀 리포트 생성
        print("\n📄 Step 4: 엑셀 리포트 생성 중...")
        reporter = ExcelReporter(processed_data)
        excel_file = reporter.generate_report()
        print(f"✅ 엑셀 리포트 생성: {excel_file}")
        
        # 5. 텔레그램 알림 발송
        print("\n📱 Step 5: 텔레그램 알림 발송 중...")
        notifier = TelegramNotifier()
        notifier.send_daily_report(alerts)
        
        # 엑셀 파일도 전송
        today = datetime.now().strftime('%Y-%m-%d')
        notifier.send_file(excel_file, f"📊 원자재/통화 상세 리포트 ({today})")
        
        print("✅ 텔레그램 알림 발송 완료")
        
        print("\n" + "=" * 50)
        print("✨ 모든 작업 완료!")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        
        # 오류 알림
        try:
            notifier = TelegramNotifier()
            notifier._send_message(
                f"🚨 시스템 오류 발생\n\n{str(e)}\n\n자세한 내용은 GitHub Actions 로그를 확인하세요.",
                silent=False
            )
        except:
            pass
        
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
