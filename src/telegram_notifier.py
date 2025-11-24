"""
텔레그램 알림 발송 모듈
"""
import requests
from datetime import datetime
from typing import List, Dict
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

class TelegramNotifier:
    """텔레그램 알림 클래스"""
    
    def __init__(self):
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def send_daily_report(self, alerts: Dict[str, List]):
        """일일 리포트 전송"""
        # Level 1: 기본 리포트 (조용히)
        if alerts['level1']:
            message = self._format_daily_report(alerts['level1'])
            self._send_message(message, silent=True)
        
        # Level 2: 주의 알림
        if alerts['level2']:
            message = "⚠️ 주의 알림\n\n" + "\n".join(alerts['level2'])
            self._send_message(message, silent=False)
        
        # Level 3: 긴급 알림 (별도 메시지, 소리+진동)
        if alerts['level3']:
            message = "🚨 긴급 알림\n\n" + "\n".join(alerts['level3'])
            self._send_message(message, silent=False)
    
    def _format_daily_report(self, report_lines: List[str]) -> str:
        """일일 리포트 포맷팅"""
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        message = f"📊 원자재/통화 일일 리포트\n"
        message += f"🕐 {now}\n"
        message += "─" * 30 + "\n\n"
        message += "\n".join(report_lines)
        message += "\n\n" + "─" * 30
        message += "\n📈 상세 리포트는 첨부된 엑셀 파일 참조"
        
        return message
    
    def _send_message(self, message: str, silent: bool = False):
        """메시지 전송"""
        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML',
                'disable_notification': silent
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ 텔레그램 전송 성공 (조용히: {silent})")
            else:
                print(f"❌ 텔레그램 전송 실패: {response.text}")
                
        except Exception as e:
            print(f"❌ 텔레그램 전송 오류: {e}")
    
    def send_file(self, filepath: str, caption: str = ""):
        """파일 전송"""
        try:
            url = f"{self.base_url}/sendDocument"
            
            with open(filepath, 'rb') as file:
                files = {'document': file}
                data = {
                    'chat_id': self.chat_id,
                    'caption': caption
                }
                
                response = requests.post(url, files=files, data=data, timeout=30)
                
                if response.status_code == 200:
                    print(f"✅ 파일 전송 성공: {filepath}")
                else:
                    print(f"❌ 파일 전송 실패: {response.text}")
                    
        except Exception as e:
            print(f"❌ 파일 전송 오류: {e}")
