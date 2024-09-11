from celery import shared_task
from time import sleep

@shared_task(ignore_result=False)
def send_invitation(invitation_id: str) -> str:
    """Send an invitation to a user via email
    """
    result = 'sent'
    sleep(100)
    return result
