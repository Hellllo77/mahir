"""Resend email helper — graceful no-op when API key absent or call fails."""
import logging

logger = logging.getLogger(__name__)


def send_invite_email(api_key: str, to_email: str, cohort_name: str, invite_url: str) -> bool:
    """Send a cohort invite email via Resend. Returns True on success, False on any failure."""
    try:
        import resend

        resend.api_key = api_key
        resend.Emails.send({
            "from": "Mahir <noreply@mahir.app>",
            "to": [to_email],
            "subject": f"You've been invited to join {cohort_name} on Mahir",
            "text": (
                f"Your teacher has invited you to join {cohort_name} on Mahir.\n\n"
                f"Click here to join: {invite_url}\n\n"
                f"This link expires in 7 days."
            ),
        })
        return True
    except Exception as exc:
        logger.warning("Resend email failed for %s: %s", to_email, exc)
        return False


def mask_api_key(key: str | None) -> str | None:
    """Return masked representation of a Resend API key, or None if not set."""
    if not key:
        return None
    if len(key) <= 8:
        return "***"
    return f"{key[:3]}***{key[-3:]}"
