from config import (
    CAMP_DATES,
    CAMP_LOCATION,
    CAMP_NAME_DISPLAY,
    FORM_PASS_SHEET,
    FORM_RESULT_SUBJECT,
    INTERVIEW_DATE_1,
    INTERVIEW_DATE_2,
    INTERVIEW_DATES,
    INTERVIEW_LOCATION,
    INTERVIEW_MAP_URL,
    INTERVIEW_REGISTRATION_LOCATION,
)
from mailer import EmailJob, run_email_job


def get_cell(row, index):
    if len(row) <= index:
        return ""

    return str(row[index]).strip()


def get_interview_schedule(row):
    interview_time_1 = get_cell(row, 2)
    interview_time_2 = get_cell(row, 3)

    if interview_time_1:
        return INTERVIEW_DATE_1, interview_time_1

    return INTERVIEW_DATE_2, interview_time_2


def log_interview_details(_name, row):
    interview_date, interview_time = get_interview_schedule(row)

    print(f"Date: {interview_date}")
    print(f"Time: {interview_time}")


def get_message(name, row):
    interview_date, interview_time = get_interview_schedule(row)

    return (
        f"เรียนคุณ {name}"
        "<br><br>🩸 ชมรมโลหิตขอขอบคุณผู้สมัครที่มีความสนใจค่ายกลางของชมรมโลหิต 🥰"
        "<br><br>ทางชมรมโลหิตมีความยินดีที่จะแจ้งว่า 🎉 "
        "<b><span style='color:#5865F2;'>คุณเป็นผู้ผ่านการคัดเลือกรอบกรอกใบสมัคร</span></b> "
        f"{CAMP_NAME_DISPLAY} ซึ่งจัดระหว่าง วันที่ {CAMP_DATES}"
        f"<br>📍{CAMP_LOCATION}"
        f"<br><br>💌ในขั้นตอนถัดไปจะมีการสัมภาษณ์ผู้สมัครในวันที่ {INTERVIEW_DATES}"
        "<br><br>โดยสำหรับวันและเวลาการสัมภาษณ์ของผู้สมัครมีรายละเอียดดังนี้"
        f"<br><br>🗓 วันที่: {interview_date}"
        f"<br>⏰ เวลา: {interview_time} น."
        f"<br>📍 สถานที่: {INTERVIEW_LOCATION} ( {INTERVIEW_MAP_URL})"
        "<br><br>ขอความกรุณาให้ผู้สมัครมาก่อนเวลาสัมภาษณ์ 15 นาที"
        f"เพื่อลงทะเบียนที่ {INTERVIEW_REGISTRATION_LOCATION}"
        "<br><br>ไว้เจอกันนะ! ✨"
        "<br>ชมรมโลหิต จุฬาลงกรณ์มหาวิทยาลัย 🩸"
    )


JOB = EmailJob(
    sheet_name=FORM_PASS_SHEET.sheet_name,
    start_row=FORM_PASS_SHEET.start_row,
    num_rows=FORM_PASS_SHEET.num_rows,
    start_col=FORM_PASS_SHEET.start_col,
    num_cols=FORM_PASS_SHEET.num_cols,
    subject=FORM_RESULT_SUBJECT,
    message_builder=get_message,
    row_logger=log_interview_details,
)


def main():
    run_email_job(JOB)


if __name__ == "__main__":
    main()
