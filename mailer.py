import smtplib
import time
from collections.abc import Callable
from dataclasses import dataclass
from html import unescape
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import gspread
from google.oauth2.service_account import Credentials

from config import APP


@dataclass(frozen=True)
class EmailJob:
    sheet_name: str
    start_row: int
    num_rows: int
    start_col: int
    num_cols: int
    subject: str
    message_builder: Callable[[str, list[str]], str]
    row_logger: Callable[[str, list[str]], None] | None = None


def get_sheet_data(job):
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly",
    ]

    creds = Credentials.from_service_account_file(
        APP.google_credentials_file,
        scopes=scopes,
    )

    client = gspread.authorize(creds)
    spreadsheet = client.open_by_url(APP.spreadsheet_url)
    sheet = spreadsheet.worksheet(job.sheet_name)

    end_row = job.start_row + job.num_rows - 1
    end_col = job.start_col + job.num_cols - 1

    start_cell = row_col_to_a1(job.start_row, job.start_col)
    end_cell = row_col_to_a1(end_row, end_col)

    return sheet.get(f"{start_cell}:{end_cell}")


def row_col_to_a1(row, col):
    letters = ""

    while col > 0:
        col, remainder = divmod(col - 1, 26)
        letters = chr(65 + remainder) + letters

    return f"{letters}{row}"


def html_to_plain_text(html_message):
    plain_message = re.sub(r"<br\s*/?>", "\n", html_message, flags=re.IGNORECASE)
    plain_message = re.sub(r"</(?:p|div)>", "\n", plain_message, flags=re.IGNORECASE)
    plain_message = re.sub(r"<[^>]+>", "", plain_message)
    return unescape(plain_message).strip()


def _validate_smtp_settings():
    if APP.sender_email == "your_email@gmail.com":
        raise RuntimeError("Set SENDER_EMAIL in .env before sending")

    if not APP.gmail_app_password or APP.gmail_app_password == "your_app_password":
        raise RuntimeError("Set GMAIL_APP_PASSWORD in .env before sending")


def _open_smtp_server():
    _validate_smtp_settings()
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

    try:
        server.login(APP.sender_email, APP.gmail_app_password)
    except Exception:
        server.quit()
        raise

    return server


def _send_message(server, msg, recipient_email):
    try:
        server.send_message(msg)
    except smtplib.SMTPResponseException as error:
        smtp_error = error.smtp_error
        if isinstance(smtp_error, bytes):
            smtp_error = smtp_error.decode("utf-8", errors="replace")

        raise RuntimeError(
            f"Gmail rejected {recipient_email} with SMTP {error.smtp_code}: {smtp_error}"
        ) from error


def send_email(recipient_email, subject, html_message, server=None):
    msg = MIMEMultipart("alternative")
    msg["From"] = APP.sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    plain_part = MIMEText(html_to_plain_text(html_message), "plain", "utf-8")
    html_part = MIMEText(html_message, "html", "utf-8")
    msg.attach(plain_part)
    msg.attach(html_part)

    if APP.dry_run:
        print("DRY RUN - email not sent")
        print(f"To: {recipient_email}")
        print(f"Subject: {subject}")
        print("-" * 50)
        return

    if server is None:
        with _open_smtp_server() as smtp_server:
            _send_message(smtp_server, msg, recipient_email)
    else:
        _send_message(server, msg, recipient_email)

    print(f"Email sent to: {recipient_email}")


def run_email_job(job):
    data = get_sheet_data(job)
    smtp_server = None

    if not APP.dry_run:
        smtp_server = _open_smtp_server()

    try:
        for i, row in enumerate(data):
            if len(row) < 2:
                continue

            name = str(row[0]).strip()
            recipient_email = str(row[1]).strip()

            if not recipient_email or recipient_email == "-":
                continue

            print(f"Process: {i + 1}")
            print(f"Name: {name}")
            print(f"Email: {recipient_email}")

            if job.row_logger is not None:
                job.row_logger(name, row)

            message = job.message_builder(name, row)
            send_email(recipient_email, job.subject, message, smtp_server)

            if not APP.dry_run and APP.email_send_delay_seconds:
                time.sleep(APP.email_send_delay_seconds)
    finally:
        if smtp_server is not None:
            smtp_server.quit()

    print("Done")
