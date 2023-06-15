from django.contrib.auth import get_user_model
from django.core import mail

from core.models.advisor import AdvisorUser
from core.models.match import Match
from core.models.startup import StartupUser
from matchProject.settings import DEFAULT_FROM_EMAIL

User = get_user_model()

ADVISOR_STARTUP_REGISTER_EMAIL_ADMIN = '''<p>Hello, Admin!</p>
<p>You have a new {} {}!</p>
<p>Review the submission by clicking <a href="https://{}" target="_blank">here</a>.</p>
<p>Att,</p><p><span style="color: var(--bs-card-color); font-size: 1rem;">&nbsp;GPr Sistemas.</span></p>
'''

ADVISOR_STARTUP_REGISTER = '''<p>Hello from Match!</p>
<p>We have received your registration submission and it is under review!</p>
<p>Att,</p><p><span style="color: var(--bs-card-color); font-size: 1rem;">&nbsp;GPr Sistemas.</span></p>
'''

ADVISOR_STARTUP_IS_ACTIVE = '''<p>Hello from Match!</p>
<p>We have news! Your profile has been approved.</p>
<p>Login to the platform by clicking <a href="https://{}" target="_blank">here</a></p>
<p>Att,</p><p><span style="color: var(--bs-card-color); font-size: 1rem;">&nbsp;GPr Sistemas.</span></p>
'''

ADVISOR_STARTUP_CONNECT_WITH = '''<p>Hello, Admin!</p>
<p>{} {} showed interest in connecting with the {} {}</p>
<p>View the match by clicking <a href="https://{}" target="_blank">here</a></p></p>
<p>Att,</p><p><span style="color: var(--bs-card-color); font-size: 1rem;">&nbsp;GPr Sistemas.</span></p>
'''


def admin_email_list() -> list:
    """
    This function will get all admin users and return your e-mail
    @return: a list with admin e-mails
    """
    staff_users = User.objects.filter(is_staff=True)
    return [user.email for user in staff_users]


def email_admin(host: str,
                user_profile: AdvisorUser or StartupUser,
                subject: str,
                cause: str,
                who_am_i: str) -> None:
    """
    This function will email admins when:
        new register -> advisor or startup
        edit profile information -> advisor or startup

    @param host: like https://devbikoffice.gpr.com.br/
    @param user_profile: the instance from Advisor or Startup
    @param subject: register or edit profile
    @param cause: register or edit profile
    @param who_am_i: string for advisor ou startup
    """

    url_path = [
        host,
        f'/settings/{who_am_i}/edit/',
        str(user_profile.id)
    ]

    email_body = ADVISOR_STARTUP_REGISTER_EMAIL_ADMIN.format(
        who_am_i,
        cause,
        ''.join(url_path)
    )

    mail.send_mail(subject=subject,
                   from_email=DEFAULT_FROM_EMAIL,
                   message=email_body,
                   recipient_list=admin_email_list(),
                   html_message=email_body)


def email_startup_advisor_register(user_email: str) -> None:
    """
    This function will email user when submit your register from home
    @param user_email: the address to which it will be sent
    """
    mail.send_mail(subject='Thank you for registration',
                   from_email=DEFAULT_FROM_EMAIL,
                   message=ADVISOR_STARTUP_REGISTER,
                   recipient_list=[user_email],
                   html_message=ADVISOR_STARTUP_REGISTER)


def email_startup_advisor_active(user_email: str, host: str) -> None:
    """
    This function will email user when admin set your status to 'Active'
    @param user_email: the address to which it will be sent
    @param host: like https://devbikoffice.gpr.com.br/
    """
    email_body = ADVISOR_STARTUP_IS_ACTIVE.format(host)

    mail.send_mail(subject='Profile approved',
                   from_email=DEFAULT_FROM_EMAIL,
                   message=email_body,
                   recipient_list=[user_email],
                   html_message=email_body)


def email_connect_with_advisor(match: Match, host: str) -> None:
    """
    This function will email admin when Advisor
    show interest to connect with Startup
    @param match: instance of the match between Advisor and Startup
    @param host: like https://devbikoffice.gpr.com.br/
    """
    if match.connect_with_advisor:

        url_path = [
            host,
            '/settings/match/'
        ]

        email_body = ADVISOR_STARTUP_CONNECT_WITH.format(
            "Startup",
            match.startup.company_name,
            "Advisor",
            match.advisor,
            ''.join(url_path)
        )

        mail.send_mail(subject='New connection interest',
                       from_email=DEFAULT_FROM_EMAIL,
                       message=email_body,
                       recipient_list=admin_email_list(),
                       html_message=email_body)


def email_connect_with_startup(match: Match, host: str):
    """
    This function will email admin when Startup
    show interest to connect with Advisor
    @param match: instance of the match between Advisor and Startup
    @param host: like https://devbikoffice.gpr.com.br/
    """
    if match.connect_with_startup:

        url_path = [
            host,
            '/settings/match/'
        ]

        email_body = ADVISOR_STARTUP_CONNECT_WITH.format(
            "Advisor",
            match.advisor,
            "Startup",
            match.startup.company_name,
            ''.join(url_path)
        )

        mail.send_mail(subject='New connection interest',
                       from_email=DEFAULT_FROM_EMAIL,
                       message=email_body,
                       recipient_list=admin_email_list(),
                       html_message=email_body)
