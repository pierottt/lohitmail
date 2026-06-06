from mailer import (
    CAMP_DATES,
    CAMP_LINE_GROUP_URL,
    CAMP_LOCATION,
    CAMP_NAME_DISPLAY,
    EmailJob,
    FIRST_MEET_DATE,
    FIRST_MEET_LOCATION,
    FIRST_MEET_MAP_URL,
    FIRST_MEET_TIME,
    INTERVIEW_RESULT_SUBJECT,
    run_email_job,
)


SHEET_NAME = "ส่งเมลผ่านสัม"
START_ROW = 2
NUM_ROWS = 25
START_COL = 1
NUM_COLS = 20


def get_message(name, _row):
    return (
        f"เรียนคุณ {name}"
        "<br><br>ชมรมโลหิตขอขอบคุณผู้สมัครที่มีความสนใจค่ายกลางของชมรมโลหิต<br><br>"
        "ทางชมรมโลหิตมีความยินดีที่จะแจ้งว่า "
        "<b><span style='color:#5865F2;'> คุณเป็นผู้ผ่านการคัดเลือกรอบสัมภาษณ์</span></b> "
        f"{CAMP_NAME_DISPLAY} ซึ่งจัดระหว่าง วันที่ {CAMP_DATES} ณ {CAMP_LOCATION}"
        "<br><br>โดยขอให้ผู้ผ่านการคัดเลือกทุกท่านเข้าร่วม "
        "<b><span style='color:#810541;'> First Meet ชาวค่าย </span></b> "
        "ที่จัดขึ้นเพื่อชี้แจงรายละเอียดค่ายและโครงให้กับผู้เข้าร่วมค่ายทุกท่าน"
        f"<br><br>วันที่: {FIRST_MEET_DATE}"
        f"<br>⏰ เวลา: {FIRST_MEET_TIME}"
        f"<br>สถานที่: {FIRST_MEET_LOCATION} ({FIRST_MEET_MAP_URL})"
        "<br><br>อย่าลืมเข้ากลุ่มไลน์ชาวค่ายนี้ด้วยนะ"
        f"<br>{CAMP_LINE_GROUP_URL}"
        "<br><br>ไว้เจอกันนะ! ✨"
        "<br>ขออภัยในความล่าช้าของการประกาศผล เนื่องจากเกิดเหตุขัดข้องทางเทคนิค"
        "<br>ชมรมโลหิต"
    )


JOB = EmailJob(
    sheet_name=SHEET_NAME,
    start_row=START_ROW,
    num_rows=NUM_ROWS,
    start_col=START_COL,
    num_cols=NUM_COLS,
    subject=INTERVIEW_RESULT_SUBJECT,
    message_builder=get_message,
)


def main():
    run_email_job(JOB)


if __name__ == "__main__":
    main()
