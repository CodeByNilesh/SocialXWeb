# chatx/utils.py

from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import EmailVerification


def send_verification_email(user, email):
    """Send OTP verification email"""
    # Generate OTP
    otp = EmailVerification.generate_otp()
    
    # Delete old unverified OTPs
    EmailVerification.objects.filter(email=email, verified=False).delete()
    
    # Create new verification record
    verification = EmailVerification.objects.create(
        user=user if (user and user.pk) else None,
        email=email,
        otp=otp
    )
    
    # Prepare email
    username = user.username if hasattr(user, 'username') else 'there'
    subject = f'SocialX Web - Your Verification Code is {otp}'
    
    message = f"""
Hi {username},

Welcome to SocialX Web!

Your verification code is:

    {otp}

This code will expire in 10 minutes.

If you didn't request this code, please ignore this email.

Best regards,
SocialX Web Team
    """
    
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 20px;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        
                        <!-- Header -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-weight: bold;">SocialX Web</h1>
                                <p style="color: #ffffff; margin: 10px 0 0 0; font-size: 14px; opacity: 0.9;">Connect. Share. Inspire.</p>
                            </td>
                        </tr>
                        
                        <!-- Content -->
                        <tr>
                            <td style="padding: 40px 30px;">
                                <h2 style="color: #333333; margin: 0 0 20px 0; font-size: 24px;">Email Verification</h2>
                                <p style="color: #666666; font-size: 16px; line-height: 24px; margin: 0 0 20px 0;">
                                    Hi <strong>{username}</strong>,
                                </p>
                                <p style="color: #666666; font-size: 16px; line-height: 24px; margin: 0 0 30px 0;">
                                    Welcome to SocialX Web! To complete your registration, please use the verification code below:
                                </p>
                                
                                <!-- OTP Box -->
                                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; padding: 30px; text-align: center; margin: 0 0 30px 0;">
                                    <p style="color: #ffffff; font-size: 14px; margin: 0 0 10px 0; text-transform: uppercase; letter-spacing: 2px;">Your Verification Code</p>
                                    <h1 style="color: #ffffff; font-size: 48px; letter-spacing: 10px; margin: 0; font-weight: bold;">{otp}</h1>
                                </div>
                                
                                <p style="color: #999999; font-size: 14px; line-height: 20px; margin: 0 0 10px 0;">
                                    ⏱️ This code will expire in <strong>10 minutes</strong>.
                                </p>
                                <p style="color: #999999; font-size: 14px; line-height: 20px; margin: 0;">
                                    🔒 For your security, never share this code with anyone.
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="background-color: #f9f9f9; padding: 30px; text-align: center; border-top: 1px solid #eeeeee;">
                                <p style="color: #999999; font-size: 12px; line-height: 18px; margin: 0 0 10px 0;">
                                    If you didn't request this code, please ignore this email or contact our support team.
                                </p>
                                <p style="color: #999999; font-size: 12px; margin: 0;">
                                    © 2025 SocialX Web. All rights reserved.
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
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=html_message,
        )
        print(f"✅ Email sent to {email} with OTP: {otp}")
        return True
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False


def verify_otp(user, email, otp):
    """Verify OTP code"""
    try:
        if user and user.pk:
            verification = EmailVerification.objects.get(
                user=user,
                email=email,
                otp=otp,
                verified=False
            )
        else:
            verification = EmailVerification.objects.get(
                email=email,
                otp=otp,
                verified=False
            )
        
        if verification.is_valid():
            verification.verified = True
            verification.save()
            return True
        else:
            return False
            
    except EmailVerification.DoesNotExist:
        return False