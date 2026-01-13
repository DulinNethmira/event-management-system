import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import List
from sqlalchemy.orm import Session
from app.api.core.config import settings
from app.api.models.event import Event, EventRegistration
from app.api.models.user import User


def send_email_otp(to_email: str, otp_code: str) -> bool:
    try:
        sender_email = settings.EMAIL_USERNAME
        sender_password = settings.EMAIL_PASSWORD
        smtp_server = settings.EMAIL_HOST
        smtp_port = settings.EMAIL_PORT

        message = MIMEMultipart("alternative")
        message["Subject"] = "Your Verification Code - Infinity Events"
        message["From"] = f"Infinity Events <{sender_email}>"
        message["To"] = to_email

        text = f"Your verification code is: {otp_code}\n\nThis code expires in 5 minutes.\n\nIf you didn't request this code, please ignore this email."
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7fa;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f7fa; padding: 40px 0;">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); overflow: hidden;">
                            
                            <tr style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                                <td style="padding: 40px 30px; text-align: center;">
                                    <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 600; letter-spacing: 0.5px;">
                                        🎉 Infinity Events
                                    </h1>
                                </td>
                            </tr>
                            
                            <tr>
                                <td style="padding: 50px 40px;">
                                    <h2 style="margin: 0 0 20px 0; color: #333333; font-size: 24px; font-weight: 600;">
                                        Verify Your Account
                                    </h2>
                                    <p style="margin: 0 0 30px 0; color: #666666; font-size: 16px; line-height: 1.6;">
                                        Thank you for signing up! Please use the verification code below to complete your registration:
                                    </p>
                                    
                                    <table width="100%" cellpadding="0" cellspacing="0">
                                        <tr>
                                            <td align="center" style="padding: 20px 0;">
                                                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; padding: 25px 40px; display: inline-block;">
                                                    <span style="color: #ffffff; font-size: 36px; font-weight: bold; letter-spacing: 8px; font-family: 'Courier New', monospace;">
                                                        {otp_code}
                                                    </span>
                                                </div>
                                            </td>
                                        </tr>
                                    </table>
                                    
                                    <div style="background-color: #fff9e6; border-left: 4px solid #ffc107; padding: 15px 20px; margin: 30px 0; border-radius: 4px;">
                                        <p style="margin: 0; color: #856404; font-size: 14px;">
                                            ⏱️ <strong>Important:</strong> This code will expire in <strong>5 minutes</strong>
                                        </p>
                                    </div>
                                    
                                    <p style="margin: 0 0 10px 0; color: #666666; font-size: 14px; line-height: 1.6;">
                                        If you didn't request this verification code, you can safely ignore this email.
                                    </p>
                                </td>
                            </tr>
                            
                            <tr style="background-color: #f8f9fa;">
                                <td style="padding: 30px 40px; text-align: center; border-top: 1px solid #e9ecef;">
                                    <p style="margin: 0 0 10px 0; color: #999999; font-size: 13px;">
                                        Need help? Contact us at support@infinityevents.com
                                    </p>
                                    <p style="margin: 0; color: #bbbbbb; font-size: 12px;">
                                        © 2026 Infinity Events. All rights reserved.
                                    </p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, message.as_string())
            
        return True

    except Exception as e:
        print(f"Email Error: {e}")
        return False


def send_event_reminder(to_email: str, user_name: str, event_title: str, 
                       event_date: str, event_location: str) -> bool:
    try:
        sender_email = settings.EMAIL_USERNAME
        sender_password = settings.EMAIL_PASSWORD
        smtp_server = settings.EMAIL_HOST
        smtp_port = settings.EMAIL_PORT

        message = MIMEMultipart("alternative")
        message["Subject"] = f"🎫 Reminder: {event_title} is Coming Up!"
        message["From"] = f"Infinity Events <{sender_email}>"
        message["To"] = to_email

        text = f"""
        Hi {user_name},
        
        This is a reminder about your upcoming event:
        
        Event: {event_title}
        Date: {event_date}
        Location: {event_location}
        
        We look forward to seeing you there!
        
        Best regards,
        Infinity Events Team
        """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7fa;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f7fa; padding: 40px 0;">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); overflow: hidden;">
                            
                            <tr style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                                <td style="padding: 40px 30px; text-align: center;">
                                    <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 600; letter-spacing: 0.5px;">
                                        🎉 Infinity Events
                                    </h1>
                                </td>
                            </tr>
                            
                            <tr>
                                <td style="padding: 50px 40px;">
                                    <h2 style="margin: 0 0 20px 0; color: #333333; font-size: 24px; font-weight: 600;">
                                        📅 Event Reminder
                                    </h2>
                                    <p style="margin: 0 0 30px 0; color: #666666; font-size: 16px; line-height: 1.6;">
                                        Hi <strong>{user_name}</strong>,
                                    </p>
                                    <p style="margin: 0 0 30px 0; color: #666666; font-size: 16px; line-height: 1.6;">
                                        This is a friendly reminder about your upcoming event! We're excited to see you there.
                                    </p>
                                    
                                    <table width="100%" cellpadding="0" cellspacing="0" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; overflow: hidden; margin: 30px 0;">
                                        <tr>
                                            <td style="padding: 35px 30px;">
                                                <h3 style="margin: 0 0 20px 0; color: #ffffff; font-size: 22px; font-weight: 600;">
                                                    {event_title}
                                                </h3>
                                                <table width="100%" cellpadding="0" cellspacing="0">
                                                    <tr>
                                                        <td style="padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.2);">
                                                            <table width="100%" cellpadding="0" cellspacing="0">
                                                                <tr>
                                                                    <td width="40" style="vertical-align: top;">
                                                                        <span style="color: #ffffff; font-size: 20px;">📅</span>
                                                                    </td>
                                                                    <td>
                                                                        <p style="margin: 0; color: rgba(255,255,255,0.8); font-size: 13px;">Date & Time</p>
                                                                        <p style="margin: 5px 0 0 0; color: #ffffff; font-size: 16px; font-weight: 500;">
                                                                            {event_date}
                                                                        </p>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="padding: 12px 0;">
                                                            <table width="100%" cellpadding="0" cellspacing="0">
                                                                <tr>
                                                                    <td width="40" style="vertical-align: top;">
                                                                        <span style="color: #ffffff; font-size: 20px;">📍</span>
                                                                    </td>
                                                                    <td>
                                                                        <p style="margin: 0; color: rgba(255,255,255,0.8); font-size: 13px;">Location</p>
                                                                        <p style="margin: 5px 0 0 0; color: #ffffff; font-size: 16px; font-weight: 500;">
                                                                            {event_location}
                                                                        </p>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                    
                                    <div style="background-color: #e8f4ff; border-left: 4px solid #2196f3; padding: 15px 20px; margin: 30px 0; border-radius: 4px;">
                                        <p style="margin: 0; color: #1976d2; font-size: 14px;">
                                            💡 <strong>Pro Tip:</strong> Save this email for quick access to your event details!
                                        </p>
                                    </div>
                                    
                                    <p style="margin: 0 0 10px 0; color: #666666; font-size: 16px; line-height: 1.6;">
                                        We're looking forward to seeing you at the event! If you have any questions, feel free to reach out to us.
                                    </p>
                                </td>
                            </tr>
                            
                            <tr style="background-color: #f8f9fa;">
                                <td style="padding: 30px 40px; text-align: center; border-top: 1px solid #e9ecef;">
                                    <p style="margin: 0 0 10px 0; color: #999999; font-size: 13px;">
                                        Need help? Contact us at support@infinityevents.com
                                    </p>
                                    <p style="margin: 0; color: #bbbbbb; font-size: 12px;">
                                        © 2026 Infinity Events. All rights reserved.
                                    </p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, message.as_string())
            
        return True

    except Exception as e:
        print(f"Email Error: {e}")
        return False


def get_upcoming_events(db: Session, days_ahead: int = 3) -> List[Event]:
    reminder_date = datetime.now() + timedelta(days=days_ahead)
    start_date = reminder_date.replace(hour=0, minute=0, second=0)
    end_date = reminder_date.replace(hour=23, minute=59, second=59)
    
    events = db.query(Event).filter(
        Event.start_time >= start_date,
        Event.start_time <= end_date
    ).all()
    
    return events


def send_reminders_for_event(db: Session, event: Event) -> int:
    registrations = db.query(EventRegistration).filter(
        EventRegistration.event_id == event.id,
        EventRegistration.reminder_sent == False
    ).all()
    
    sent_count = 0
    
    for registration in registrations:
        user = db.query(User).filter(User.user_id == registration.user_id).first()
        
        if user and user.email:
            success = send_event_reminder(
                to_email=user.email,
                user_name=user.name,
                event_title=event.title,
                event_date=event.start_time.strftime("%B %d, %Y at %I:%M %p"),
                event_location=event.location
            )
            
            if success:
                registration.reminder_sent = True
                db.commit()
                sent_count += 1
    
    return sent_count


async def run_reminder_job(db: Session):
    print(f"Starting reminder job at {datetime.now()}")
    
    events = get_upcoming_events(db, days_ahead=3)
    
    total_sent = 0
    for event in events:
        sent = send_reminders_for_event(db, event)
        total_sent += sent
        print(f"Sent {sent} reminders for event: {event.title}")
    
    print(f"Total reminders sent: {total_sent}")