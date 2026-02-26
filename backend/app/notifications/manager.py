"""
Sistema de Notificações Multi-Canal
Telegram, Email (SendGrid) e WhatsApp (Twilio)
"""
import asyncio
import logging
from typing import List, Dict, Optional
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from twilio.rest import Client
from app.config import settings

logger = logging.getLogger(__name__)


# runtime configuration object (mutable) separate from settings
class NotificationRuntimeConfig:
    telegram_token: Optional[str] = None
    telegram_chat_ids: Optional[List[str]] = None
    email_to: Optional[List[str]] = None
    sendgrid_key: Optional[str] = None
    twilio_sid: Optional[str] = None
    whatsapp_numbers: Optional[List[str]] = None

runtime_config = NotificationRuntimeConfig()


class NotificationManager:
    """Gerenciador centralizado de notificações"""
    
    def __init__(self):
        self.telegram = TelegramNotifier()
        self.email = EmailNotifier()  
        self.whatsapp = WhatsAppNotifier()
    
    async def send_alert(self, alert: Dict, channels: List[str] = None) -> Dict:
        """
        Envia alerta por múltiplos canais
        
        Args:
            alert: Dicionário com dados do alerta
            channels: Lista de canais ['telegram', 'email', 'whatsapp']
            
        Returns:
            Dict com status de envio
        """
        if channels is None:
            channels = ['telegram', 'email', 'whatsapp']
        
        results = {}
        
        # Telegram
        if 'telegram' in channels:
            results['telegram'] = await self.telegram.send_alert(alert)
        
        # Email
        if 'email' in channels:
            results['email'] = await self.email.send_alert(alert)
        
        # WhatsApp
        if 'whatsapp' in channels:
            results['whatsapp'] = await self.whatsapp.send_alert(alert)
        
        return results
    
    async def send_heartbeat(self) -> None:
        """Envia heartbeat de status"""
        heartbeat = {
            'type': 'heartbeat',
            'timestamp': datetime.now().isoformat(),
            'message': '✅ SMC está operacional'
        }
        
        await self.send_alert(heartbeat)


class TelegramNotifier:
    """Notificador via Telegram"""
    
    def __init__(self):
        # initialization only sets up placeholders; actual tokens
        # are retrieved each time send_alert is called so runtime
        # configuration changes take effect immediately.
        self.bot = None

    async def send_alert(self, alert: Dict) -> Dict:
        bot_token = runtime_config.telegram_token or settings.TELEGRAM_BOT_TOKEN
        chat_ids = runtime_config.telegram_chat_ids or settings.get_telegram_chat_ids()
        if not bot_token or not chat_ids:
            return {
                'status': 'skipped',
                'reason': 'Telegram não configurado'
            }
        # lazy-initialize bot with current token
        self.bot = Bot(token=bot_token)
        try:
            message = self._format_message(alert)
            for chat_id in chat_ids:
                try:
                    await self.bot.send_message(
                        chat_id=chat_id,
                        text=message,
                        parse_mode='HTML'
                    )
                except TelegramError as e:
                    logger.error(f"Erro ao enviar para {chat_id}: {str(e)}")
            return {'status': 'success', 'count': len(chat_ids)}
        except Exception as e:
            logger.error(f"Erro TelegramNotifier: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    
    def _format_message(self, alert: Dict) -> str:
        """Formata mensagem para Telegram"""
        alert_type = alert.get('type', 'unknown')
        
        if alert_type == 'buy_signal':
            emoji = '🟢'
            text = f"{emoji} <b>SETUP DE COMPRA</b>\n"
        elif alert_type == 'sell_signal':
            emoji = '🔴'
            text = f"{emoji} <b>SETUP DE VENDA</b>\n"
        elif alert_type == 'warning':
            emoji = '⚠️'
            text = f"{emoji} <b>AVISO</b>\n"
        elif alert_type == 'trap':
            emoji = '💥'
            text = f"{emoji} <b>ARMADILHA DETECTADA</b>\n"
        else:
            text = f"<b>{alert_type.upper()}</b>\n"
        
        text += f"\n<b>Timestamp:</b> {alert.get('timestamp', 'N/A')}"
        text += f"\n<b>Score:</b> {alert.get('score', 'N/A')}"
        text += f"\n<b>Preço:</b> {alert.get('price', 'N/A')}"
        text += f"\n<b>Detalhes:</b> {alert.get('message', 'N/A')}"
        
        return text


class EmailNotifier:
    """Notificador via Email (SendGrid)"""
    
    def __init__(self):
        self.client = None

    async def send_alert(self, alert: Dict) -> Dict:
        api_key = runtime_config.sendgrid_key or settings.SENDGRID_API_KEY
        from_email = settings.EMAIL_FROM
        to_addresses = runtime_config.email_to or settings.get_email_to_addresses()
        if not api_key or not to_addresses:
            return {
                'status': 'skipped',
                'reason': 'Email não configurado'
            }
        self.client = SendGridAPIClient(api_key)
        try:
            subject, html_content = self._format_email(alert)
            for to_email in to_addresses:
                message = Mail(
                    from_email=Email(from_email),
                    to_emails=To(to_email),
                    subject=subject,
                    html_content=html_content
                )
                try:
                    self.client.send(message)
                except Exception as e:
                    logger.error(f"Erro ao enviar email para {to_email}: {str(e)}")
            return {'status': 'success', 'count': len(to_addresses)}
        except Exception as e:
            logger.error(f"Erro EmailNotifier: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    async def send_alert(self, alert: Dict) -> Dict:
        """Envia alerta via Email"""
        if not self.api_key or not self.to_addresses:
            return {
                'status': 'skipped',
                'reason': 'Email não configurado'
            }
        
        try:
            subject, html_content = self._format_email(alert)
            
            for to_email in self.to_addresses:
                message = Mail(
                    from_email=Email(self.from_email),
                    to_emails=To(to_email),
                    subject=subject,
                    html_content=html_content
                )
                
                try:
                    response = self.client.send(message)
                except Exception as e:
                    logger.error(f"Erro ao enviar email para {to_email}: {str(e)}")
            
            return {'status': 'success', 'count': len(self.to_addresses)}
        
        except Exception as e:
            logger.error(f"Erro EmailNotifier: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def _format_email(self, alert: Dict) -> tuple:
        """Formata email HTML"""
        alert_type = alert.get('type', 'unknown')
        
        # Subject
        if alert_type == 'buy_signal':
            subject = "🟢 SETUP DE COMPRA - SMC Analysis"
        elif alert_type == 'sell_signal':
            subject = "🔴 SETUP DE VENDA - SMC Analysis"
        else:
            subject = f"SMC - {alert_type.upper()}"
        
        # HTML
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>{subject}</h2>
                <hr>
                <p><b>Timestamp:</b> {alert.get('timestamp', 'N/A')}</p>
                <p><b>Tipo:</b> {alert_type.upper()}</p>
                <p><b>Score:</b> {alert.get('score', 'N/A')}</p>
                <p><b>Preço:</b> {alert.get('price', 'N/A')}</p>
                <p><b>Detalhes:</b></p>
                <pre>{alert.get('message', 'N/A')}</pre>
                <hr>
                <p><small>SMC - Sistema de Monitoramento Contínuo de Mercado</small></p>
            </body>
        </html>
        """
        
        return subject, html


class WhatsAppNotifier:
    """Notificador via WhatsApp (Twilio)"""
    
    def __init__(self):
        self.client = None

    async def send_alert(self, alert: Dict) -> Dict:
        account_sid = runtime_config.twilio_sid or settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        from_number = settings.TWILIO_PHONE_NUMBER
        to_numbers = runtime_config.whatsapp_numbers or settings.get_whatsapp_numbers()
        if not account_sid or not auth_token or not from_number or not to_numbers:
            return {
                'status': 'skipped',
                'reason': 'WhatsApp não configurado'
            }
        self.client = Client(account_sid, auth_token)
        try:
            message_text = self._format_message(alert)
            for to_number in to_numbers:
                try:
                    self.client.messages.create(
                        from_=f"whatsapp:{from_number}",
                        to=f"whatsapp:{to_number}",
                        body=message_text
                    )
                except Exception as e:
                    logger.error(f"Erro ao enviar WhatsApp para {to_number}: {str(e)}")
            return {'status': 'success', 'count': len(to_numbers)}
        except Exception as e:
            logger.error(f"Erro WhatsAppNotifier: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def _format_message(self, alert: Dict) -> str:
        """Formata mensagem WhatsApp"""
        alert_type = alert.get('type', 'unknown')
        
        if alert_type == 'buy_signal':
            text = "🟢 SETUP DE COMPRA\n"
        elif alert_type == 'sell_signal':
            text = "🔴 SETUP DE VENDA\n"
        elif alert_type == 'trap':
            text = "💥 ARMADILHA!\n"
        else:
            text = f"{alert_type.upper()}\n"
        
        text += f"\nPreço: {alert.get('price', 'N/A')}"
        text += f"\nScore: {alert.get('score', 'N/A')}"
        text += f"\n{alert.get('message', 'N/A')}"
        text += f"\n\n⏰ {alert.get('timestamp', 'N/A')}"
        
        return text


# Instância única
notification_manager = NotificationManager()
