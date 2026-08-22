from config import CAMP_NAME, FORM_FAIL_SHEET, FORM_RESULT_SUBJECT
from mailer import EmailJob, run_email_job


def get_message(name, _row):
    return (
        f"เรียนคุณ {name}"
        f'<br><br>🩸ชมรมโลหิตขอขอบคุณอย่างยิ่งสำหรับความสนใจในการสมัครเข้าร่วม "{CAMP_NAME}" ในครั้งนี้🙏🏻'
        "<br><br>เราได้อ่านใบสมัครของคุณด้วยความประทับใจ และเห็นถึงความตั้งใจที่อยากมาร่วมทำสิ่งดี ๆ ไปด้วยกัน "
        "แต่เนื่องจากมีผู้สมัครจำนวนมากเกินกว่าที่ค่ายจะสามารถรองรับได้ "
        "ทางชมรมจึงขอแสดงความเสียใจที่ต้องแจ้งให้ทราบว่า "
        "<b><span style='color:#990000;'>คุณยังไม่ได้รับการคัดเลือกในครั้งนี้</span></b>"
        "<br><br>ถึงแม้จะยังไม่ได้เข้าร่วมค่ายในรอบนี้ แต่เราอยากขอให้คุณภูมิใจกับความตั้งใจ"
        "และความพยายามของตัวเอง ทุกก้าวเล็ก ๆ ที่คุณเลือกทำเพื่อตัวเองและผู้อื่นนั้นมีความหมายเสมอ 🤲🏻🤍"
        "<br><br>ชมรมโลหิตขอเป็นกำลังใจให้คุณในทุกสิ่งที่ตั้งใจทำ "
        "และหวังว่าจะได้พบกันอีกในค่ายหน้า"
        "<br><br>ขอแสดงความนับถือ"
        "<br>ชมรมโลหิต จุฬาลงกรณ์มหาวิทยาลัย🩸"
    )


JOB = EmailJob(
    sheet_name=FORM_FAIL_SHEET.sheet_name,
    start_row=FORM_FAIL_SHEET.start_row,
    num_rows=FORM_FAIL_SHEET.num_rows,
    start_col=FORM_FAIL_SHEET.start_col,
    num_cols=FORM_FAIL_SHEET.num_cols,
    subject=FORM_RESULT_SUBJECT,
    message_builder=get_message,
)


def main():
    run_email_job(JOB)


if __name__ == "__main__":
    main()
