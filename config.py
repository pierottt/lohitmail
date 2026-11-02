"""Application and campaign configuration.

Keep secrets and machine-specific values in ``.env``. Campaign copy and sheet
ranges live here so the mailer and individual jobs do not duplicate settings.
"""

from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv


load_dotenv(override=True)


def _required_env(name: str) -> str:
    value = getenv(name)

    if value is None or value.strip() == "":
        raise RuntimeError(f"Missing required environment variable: {name}")

    return value


def _bool_env(name: str, default: bool) -> bool:
    value = getenv(name)

    if value is None or value.strip() == "":
        return default

    normalized_value = value.strip().lower()

    if normalized_value in {"1", "true", "yes", "y", "on"}:
        return True

    if normalized_value in {"0", "false", "no", "n", "off"}:
        return False

    raise RuntimeError(f"{name} must be true or false")


def _float_env(name: str, default: float) -> float:
    value = getenv(name)

    if value is None or value.strip() == "":
        return default

    try:
        parsed_value = float(value)
    except ValueError as error:
        raise RuntimeError(f"{name} must be a number") from error

    if parsed_value < 0:
        raise RuntimeError(f"{name} must be zero or greater")

    return parsed_value


@dataclass(frozen=True)
class AppConfig:
    spreadsheet_url: str
    google_credentials_file: str
    sender_email: str
    gmail_app_password: str
    dry_run: bool
    email_send_delay_seconds: float


@dataclass(frozen=True)
class SheetRange:
    sheet_name: str
    start_row: int
    num_rows: int
    start_col: int = 1
    num_cols: int = 20


APP = AppConfig(
    spreadsheet_url=_required_env("SPREADSHEET_URL"),
    google_credentials_file=getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json"),
    sender_email=_required_env("SENDER_EMAIL"),
    gmail_app_password=getenv("GMAIL_APP_PASSWORD", ""),
    dry_run=_bool_env("DRY_RUN", True),
    email_send_delay_seconds=_float_env("EMAIL_SEND_DELAY_SECONDS", 1.0),
)

CAMP_NAME = "พริกป่น พริกไทย พลิกไป พลิกมา ลมหนาวนำพา ปิ๊กมาแม่พริก"
CAMP_NAME_DISPLAY = f"⛰️{CAMP_NAME}⛅️"
CAMP_DATES = "17-27 ธันวาคม 2569"
CAMP_LOCATION = "โรงเรียน โรงเรียนบ้านแม่พริก ต.วังใต้ อ.วังเหนือ จ.ลำปาง"

CONFIRMATION_DEADLINE = "2 กันยายน เวลา 23.59 น."
CONFIRMATION_FORM_URL = "https://forms.gle/ZDtmdwPKyqQgb3Tm8"

FIRST_MEET_DATE = "วันศุกร์ที่ 4 กันยายน 2569"
FIRST_MEET_TIME = "เริ่มลงทะเบียน 16.45 กิจกรรม 17.00-19.30 น."
FIRST_MEET_LOCATION = "CU Plearn Space"
FIRST_MEET_MAP_URL = "https://maps.app.goo.gl/Ygx5Ykq958tVnYyL6?g_st=ic"

INTERVIEW_DATE_1 = "วันพุธที่ 4 พฤศจิกายน 2569"
INTERVIEW_DATE_2 = "วันพฤหัสบดีที่ 5 พฤศจิกายน 2569"
INTERVIEW_DATES = "4-5 พฤศจิกายน 2569"
INTERVIEW_LOCATION = "สำนักงานวิทยทรัพยากร จุฬาลงกรณ์มหาวิทยาลัย ชั้น 2"
INTERVIEW_REGISTRATION_LOCATION = "สำนักงานวิทยทรัพยากร จุฬาลงกรณ์มหาวิทยาลัย ชั้น 2"
INTERVIEW_MAP_URL = "https://maps.app.goo.gl/fymBWbNStnkpnqJz7?g_st=ic"

NEW_INTERVIEW_LOCATION_MAP_URL = "https://maps.app.goo.gl/dSj2enQbgnB2ZKbMA?g_st=il"

FORM_RESULT_SUBJECT = f"ประกาศผลการคัดเลือกรอบฟอร์ม {CAMP_NAME_DISPLAY}"

# FORM_PASS_SHEET = SheetRange("test", start_row=3, num_rows=1)
FORM_PASS_SHEET = SheetRange("ส่งเมลผ่านฟอร์ม", start_row=5, num_rows=72)


# FORM_FAIL_SHEET = SheetRange("test", start_row=3, num_rows=1)
FORM_FAIL_SHEET = SheetRange("ส่งเมลไม่ผ่านฟอร์ม", start_row=5, num_rows=102)

# for emergency change interview location
new_interview_location = "ใต้โถงอาคารพินิตประชานาถ คณะนิติศาสตร์"
INTERVIEW_RESULT_SUBJECT = f"ประกาศผลการคัดเลือกรอบสัมภาษณ์ {CAMP_NAME_DISPLAY}"
# CHANGE_LOCATION_SHEET = SheetRange("ส่งเมลผ่านฟอร์ม", start_row=2, num_rows=1)
CHANGE_LOCATION_SHEET = SheetRange("ส่งเมลผ่านฟอร์ม", start_row=5, num_rows=72)


INTERVIEW_PASS_SHEET = SheetRange("ส่งเมลผ่านสัม", start_row=5, num_rows=23)
INTERVIEW_FAIL_SHEET = SheetRange("ส่งเมลไม่ผ่านสัม", start_row=5, num_rows=57)
