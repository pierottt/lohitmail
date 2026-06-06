from mailer import (
    CAMP_NAME_DISPLAY,
    EmailJob,
    INTERVIEW_RESULT_SUBJECT,
    run_email_job,
)


SHEET_NAME = "ส่งเมลไม่ผ่านสัม"
START_ROW = 2
NUM_ROWS = 36
START_COL = 1
NUM_COLS = 20


def get_message(name, _row):
    return (
        f"เรียนคุณ {name}"
        "<br><br>ชมรมโลหิตขอขอบคุณผู้สมัครที่มีความสนใจค่ายกลางของชมรมโลหิต<br><br>"
        "ทางชมรมโลหิตขอแสดงความเสียใจที่ "
        "<b><span style='color:#990000;'> คุณไม่ผ่านการคัดเลือกรอบสัมภาษณ์</span></b> "
        f"{CAMP_NAME_DISPLAY} เนื่องจากผู้สมัครมีจำนวนมากเกินกว่าที่ทางค่ายจะรองรับได้"
        "<br><br>หากมีโอกาสหน้า อย่าลืมมาสมัครค่ายของชมรมโลหิตอีกนะ ✨"
        "<br><br>หวังว่าจะได้เจอกันในโอกาสหน้านะ"
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
