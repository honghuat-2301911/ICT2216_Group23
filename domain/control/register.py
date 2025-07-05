"""User registration control logic and business rules"""

from data_source.user_queries import get_user_by_email, insert_user, update_user_verification_status
from itsdangerous import URLSafeTimedSerializer
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from flask import current_app, url_for

def get_serializer():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

def register_user(user_data: dict) -> bool:
    # TODO: Implement register function
    existing_user = get_user_by_email(user_data["email"])
    if existing_user:
        print("User already exists with this email.")
        return False
    return insert_user(user_data)


def generate_verification_token(email):
    serializer = get_serializer()
    return serializer.dumps(email, salt='email-verify')


def send_verification_email(user_email, token):
    verify_url = url_for('register.verify_email', token=token, _external=True)
    message = Mail(
        from_email='buddiesfinder@gmail.com',
        to_emails=user_email,
        subject='Verify Your Email',
        html_content=f'<p>Click to verify: <a href="{verify_url}">{verify_url}</a></p>'
    )
    try:
        api_key = os.getenv('EMAILVERIFICATION_API_KEY')
        current_app.logger.error(f"api key: {api_key}")
        sg = SendGridAPIClient(api_key)

        response = sg.send(message)    
        current_app.logger.error(f"response status code:{response.status_code}")
        current_app.logger.error(f"response body:{response.body}")  
        current_app.logger.error(f"response header:{response.headers}")  
        
    except Exception as e:
        current_app.logger.error(f"Error sending verification email: {e}")


def update_verification_status(email, verified=True):
    return update_user_verification_status(email, verified)
