from mailer import (
    CAMP_DATES,
    CAMP_LOCATION,
    CAMP_NAME_DISPLAY,
    EmailJob,
    FORM_RESULT_SUBJECT,
    run_email_job,
)


SHEET_NAME = "ส่งเมลผ่านสัม"
START_ROW = 2
NUM_ROWS = 60
START_COL = 1
NUM_COLS = 20

INTERVIEW_DATE_1 = "วันพุธที่ 29 ตุลาคม 2568"
INTERVIEW_DATE_2 = "วันพฤหัสบดีที่ 30 ตุลาคม 2568"
INTERVIEW_DATES = "29-30 ตุลาคม 2568"
INTERVIEW_LOCATION = "อาคารเจริญวิศวกรรม (ตึก 4) คณะวิศวกรรมศาสตร์"
INTERVIEW_MAP_URL = "https://maps.app.goo.gl/TGmqqsZoMFKj9fpWA"


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
        "<br><br> ชมรมโลหิตขอขอบคุณผู้สมัครที่มีความสนใจค่ายกลางของชมรมโลหิต <br><br>"
        "ทางชมรมโลหิตมีความยินดีที่จะแจ้งว่า  "
        "<b><span style='color:#5865F2;'> คุณเป็นผู้ผ่านการคัดเลือกรอบกรอกใบสมัคร</span></b> "
        f"{CAMP_NAME_DISPLAY} ซึ่งจัดระหว่าง วันที่ {CAMP_DATES} ณ {CAMP_LOCATION}"
        f"<br><br>ในขั้นตอนถัดไปจะมีการสัมภาษณ์ผู้สมัครในวันที่ {INTERVIEW_DATES} "
        "<br><br>โดยสำหรับวันและเวลาการสัมภาษณ์ของผู้สมัครมีรายละเอียดดังนี้"
        f"<br><br> วันที่: {interview_date}"
        f"<br>⏰ เวลา: {interview_time} น."
        f"<br> สถานที่: {INTERVIEW_LOCATION} ({INTERVIEW_MAP_URL})"
        f"<br><br>ขอความกรุณาให้ผู้สมัครมาก่อนเวลาสัมภาษณ์ 15 นาทีเพื่อลงทะเบียนที่ {INTERVIEW_LOCATION}"
        "<br><br>ไว้เจอกันนะ! ✨"
        "<br>ชมรมโลหิต"
    )


JOB = EmailJob(
    sheet_name=SHEET_NAME,
    start_row=START_ROW,
    num_rows=NUM_ROWS,
    start_col=START_COL,
    num_cols=NUM_COLS,
    subject=FORM_RESULT_SUBJECT,
    message_builder=get_message,
    row_logger=log_interview_details,
)


def main():
    run_email_job(JOB)


if __name__ == "__main__":
    main()
