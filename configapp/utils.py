import random
from django.core.mail import send_mail


def send_otp(email):
    otp = random.randint(100000, 999999)
    send_mail(
        'Your OTP Code',
        f'Your OTP code is {otp}',
        'from@example.com',
        [email],
        fail_silently=False,
    )
    return otp


def verify_otp(input_otp, correct_otp):
    return input_otp == correct_otp
