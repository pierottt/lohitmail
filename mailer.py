import smtplib
from collections.abc import Callable
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import getenv

import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials


load_dotenv()


def get_required_env(name):
    value = getenv(name)

    if value is None or value.strip() == "":
        raise RuntimeError(f"Missing required environment variable: {name}")

    return value


def get_bool_env(name, default):
    value = getenv(name)

    if value is None or value.strip() == "":
        return default

    normalized_value = value.strip().lower()

    if normalized_value in {"1", "true", "yes", "y", "on"}:
        return True

    if normalized_value in {"0", "false", "no", "n", "off"}:
        return False

    raise RuntimeError(f"{name} must be true or false")


SPREADSHEET_URL = get_required_env("SPREADSHEET_URL")
GOOGLE_CREDENTIALS_FILE = getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")

SENDER_EMAIL = get_required_env("SENDER_EMAIL")
GMAIL_APP_PASSWORD = getenv("GMAIL_APP_PASSWORD", "")
DRY_RUN = get_bool_env("DRY_RUN", True)

CAMP_NAME = "ค่ายไม่ว่าปางนี้หรือปางไหน อยากให้เธอมาพักใจที่ปางหลวง"
CAMP_NAME_DISPLAY = f"{CAMP_NAME}🌦️"
CAMP_DATES = "16-27 ธันวาคม 2568"
CAMP_LOCATION = "โรงเรียนบ้านปางหลวง ต.ท่าก๊อ อ.แม่สรวย จ.เชียงราย"

FIRST_MEET_DATE = "วันศุกร์ที่ 7 พฤศจิกายน 2568"
FIRST_MEET_TIME = "16.50-19.30 น."
FIRST_MEET_LOCATION = "ห้อง 406 อาคารจามจุรี 9"
FIRST_MEET_MAP_URL = "https://maps.app.goo.gl/e5Eji81xqeLEkYUCA?g_st=ipc"

CAMP_LINE_GROUP_URL = "https://line.me/ti/g/QneAzQsYRB"

INTERVIEW_RESULT_SUBJECT = f"ประกาศผลการคัดเลือกรอบสัมภาษณ์ {CAMP_NAME_DISPLAY}"
FORM_RESULT_SUBJECT = f"ประกาศผลการคัดเลือกรอบกรอกใบสมัคร {CAMP_NAME_DISPLAY}"


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
        GOOGLE_CREDENTIALS_FILE,
        scopes=scopes,
    )

    client = gspread.authorize(creds)
    spreadsheet = client.open_by_url(SPREADSHEET_URL)
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


def send_email(recipient_email, subject, html_message):
    msg = MIMEMultipart("alternative")
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient_email
    msg["Subject"] = subject

    html_part = MIMEText(html_message, "html", "utf-8")
    msg.attach(html_part)

    if DRY_RUN:
        print("DRY RUN - email not sent")
        print(f"To: {recipient_email}")
        print(f"Subject: {subject}")
        print("-" * 50)
        return

    if SENDER_EMAIL == "your_email@gmail.com":
        raise RuntimeError("Set SENDER_EMAIL in .env before sending")

    if not GMAIL_APP_PASSWORD or GMAIL_APP_PASSWORD == "your_app_password":
        raise RuntimeError("Set GMAIL_APP_PASSWORD in .env before sending")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, GMAIL_APP_PASSWORD)
        server.send_message(msg)

    print(f"Email sent to: {recipient_email}")


def run_email_job(job):
    data = get_sheet_data(job)

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
        send_email(recipient_email, job.subject, message)

    print("Done")
