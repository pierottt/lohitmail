from mailer import (
    CAMP_NAME,
    EmailJob,
    FORM_RESULT_SUBJECT,
    run_email_job,
)


SHEET_NAME = "ส่งเมลไม่ผ่านสัม"
START_ROW = 38
NUM_ROWS = 47
START_COL = 1
NUM_COLS = 20


def get_message(name, _row):
    return (
        f"เรียนคุณ {name}"
        f"<br><br>ชมรมโลหิตขอขอบคุณอย่างยิ่งสำหรับความสนใจในการสมัครเข้าร่วม “{CAMP_NAME}ของชมรมโลหิต” ในครั้งนี้ "
        "<br><br>เราได้อ่านใบสมัครของคุณด้วยความประทับใจ และเห็นถึงความตั้งใจที่อยากมาร่วมทำสิ่งดีๆไปด้วยกัน "
        "แต่เนื่องจากมีผู้สมัครจำนวนมากเกินกว่าที่ค่ายจะสามารถรองรับได้"
        "<br>ทางชมรมจึงขอแสดงความเสียใจที่ต้องแจ้งให้ทราบว่า "
        "<b><span style='color:#990000;'> คุณยังไม่ได้รับการคัดเลือกในครั้งนี้</span></b>"
        "<br><br>ถึงแม้จะยังไม่ได้เข้าร่วมค่ายในรอบนี้ แต่เราอยากขอให้คุณภูมิใจกับความตั้งใจและความพยายามของตัวเอง "
        "ทุกก้าวเล็กๆ ที่คุณเลือกทำเพื่อตัวเองและผู้อื่นนั้นมีความหมายเสมอ"
        "<br><br>โลหิตขอเป็นกำลังใจให้คุณในทุกสิ่งที่ตั้งใจทำ และหวังว่าจะได้พบกันอีกในค่ายหน้า"
        "<br><br>ขอแสดงความนับถือ"
        "<br>ชมรมโลหิต จุฬาลงกรณ์มหาวิทยาลัย"
    )


JOB = EmailJob(
    sheet_name=SHEET_NAME,
    start_row=START_ROW,
    num_rows=NUM_ROWS,
    start_col=START_COL,
    num_cols=NUM_COLS,
    subject=FORM_RESULT_SUBJECT,
    message_builder=get_message,
)


def main():
    run_email_job(JOB)


if __name__ == "__main__":
    main()
