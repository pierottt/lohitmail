from config import (
    CHANGE_LOCATION_SHEET,
    NEW_INTERVIEW_LOCATION_MAP_URL,
    new_interview_location,
)
from mailer import EmailJob, run_email_job


SUBJECT = "แจ้งเปลี่ยนแปลงสถานที่สัมภาษณ์"


def get_message(name, _row):
    return (
        f"เรียนคุณ {name}"
        "<br><br>📢 ขอแจ้งเปลี่ยนแปลงสถานที่สัมภาษณ์"
        "<br><b><span style='color:#990000;'>สถานที่สัมภาษณ์ใหม่:</span></b>"
        f"<br><b>📍 {new_interview_location}</b> "
        f"(<a href='{NEW_INTERVIEW_LOCATION_MAP_URL}'>{NEW_INTERVIEW_LOCATION_MAP_URL}</a>)"
        "<br><br><b>หมายเหตุ: วันและเวลาสัมภาษณ์ยังคงเดิม ไม่มีการเปลี่ยนแปลง</b>"
        "<br><br>ขออภัยในความไม่สะดวก และขอความกรุณาตรวจสอบสถานที่ใหม่ก่อนเดินทาง"
        "<br><br>ขอบคุณครับ/ค่ะ"
        "<br>ชมรมโลหิต จุฬาลงกรณ์มหาวิทยาลัย 🩸"
    )


JOB = EmailJob(
    sheet_name=CHANGE_LOCATION_SHEET.sheet_name,
    start_row=CHANGE_LOCATION_SHEET.start_row,
    num_rows=CHANGE_LOCATION_SHEET.num_rows,
    start_col=CHANGE_LOCATION_SHEET.start_col,
    num_cols=CHANGE_LOCATION_SHEET.num_cols,
    subject=SUBJECT,
    message_builder=get_message,
)


def main():
    run_email_job(JOB)


if __name__ == "__main__":
    main()
