from celery import shared_task
from flask_mail import Message
from flask import current_app
from v1.controllers.event import get_event
from time import sleep

@shared_task(ignore_result=False)
def send_invitation(invitation: dict | list[dict]) -> None:
    """Send an invitation to a user via email
    """
    if isinstance(invitation, dict):
        print("Invitation is being sent")
        event = get_event(invitation.get("event_id"))
        try:
            send_mail(invitation, event.to_dict())
            return
        except Exception:
            raise
    print("Invitations are being sent")
    event = get_event(invitation[0].get("event_id"))
    try:
        send_bulk_mail(invitation, event.to_dict())
        return
    except Exception:
        raise

def send_mail(invitation: dict, event: dict) -> None:
    """Send mail function
    """
    if event:
        subject = f"It is an honor to invite you to {event.get('event_name')}"
    else:
        subject = "It is an honor to invite you to the event"
    msg = Message(
        subject=subject,
        sender="justinoghenekomeebedi@gmail.com",
        recipients=[invitation['recipient_email']]
    )
    msg.body = f"{invitation.get('message')}\nKindly click the link below to respond to your invitation\nhttp://localhost:3000/rsvp/{invitation['id']}/{event['id']}"
    mail = current_app.mail
    with current_app.app_context():
        counter = 0
        while counter < 5:
            try:
                mail.send(msg)
                return "Sent"
            except ConnectionRefusedError:
                mail.send(msg)
            except Exception as e:
                print(str(e))
            finally:
                counter += 1
        return "Not sent"

def send_bulk_mail(invitations: list[dict], event: dict) -> None:
    """Send multiple email
    """
    if event:
        subject = f"It is an honor to invite you to {event.get('event_name')}"
    else:
        subject = "It is an honor to invite you to the event"
    mail = current_app.mail
    with mail.connect() as conn:
        email_count = 0
        print("Number of invitations", len(invitations))
        for invitation in invitations:
            msg = Message(
                subject=subject,
                sender="justinoghenekomeebedi@gmail.com",
                recipients=[invitation['recipient_email']]
            )
            msg.body = f"{invitation.get('message')}\nKindly click this link to RSVP http://localhost:3000/rsvp/{invitation.get('id')}/{invitation.get('event_id')}"
            with current_app.app_context():
                counter = 0
                while counter < 5:
                    sleep(1)
                    try:
                        conn.send(msg)
                        email_count += 1
                        break
                    except ConnectionRefusedError:
                        mail.send(msg)
                    except Exception as e:
                        print(str(e))
                    finally:
                        counter += 1
            print("1 invitation has been sent for the event")
            print("Number of emails sent", email_count)
            sleep(1)
