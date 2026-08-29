from config import (
    CAMP_DATES,
    CAMP_LOCATION,
    CAMP_NAME_DISPLAY,
    CONFIRMATION_DEADLINE,
    CONFIRMATION_FORM_URL,
    FIRST_MEET_DATE,
    FIRST_MEET_TIME,
    INTERVIEW_PASS_SHEET,
    INTERVIEW_RESULT_SUBJECT,
)
from mailer import EmailJob, run_email_job


def get_message(name, _row):
    return (
        f"เรียนคุณ {name}"
        "<br><br>🩸 ชมรมโลหิตขอขอบคุณผู้สมัครที่มีความสนใจค่ายต้นของชมรมโลหิต 🥰"
        "<br><br>ทางชมรมโลหิตมีความยินดีที่จะแจ้งว่า 🎉 "
        "<b><span style='color:#5865F2;'>คุณเป็นผู้ผ่านการคัดเลือกรอบสัมภาษณ์</span></b> "
        f"{CAMP_NAME_DISPLAY} ซึ่งจัดระหว่าง วันที่ {CAMP_DATES} ณ 📍{CAMP_LOCATION}"
        "<br><br>ขอให้ผู้ผ่านการคัดเลือกกดยืนยันสิทธิผ่านทางการกรอกฟอร์มอีกครั้ง"
        f"พร้อมชำระค่ามัดจำภายในวันที่ {CONFIRMATION_DEADLINE}"
        f"<br>📌 {CONFIRMATION_FORM_URL} 📌"
        "<br><br>📢 โดยขอให้ผู้ผ่านการคัดเลือกทุกท่านเข้าร่วม "
        "<b><span style='color:#810541;'>First Meet ชาวค่าย</span></b> "
        "ที่จัดขึ้นเพื่อชี้แจงรายละเอียดค่ายและโครงให้กับผู้เข้าร่วมค่ายทุกท่าน"
        f"<br><br>🗓️วันที่: {FIRST_MEET_DATE}"
        f"<br>⏰เวลา: {FIRST_MEET_TIME}"
        "<br>โดยสถานที่จะแจ้งให้ทราบอีกครั้งในกลุ่มไลน์"
        "<br><br>💌อย่าลืมเข้ากลุ่มไลน์ชาวค่ายนี้ด้วยนะ ! "
        "🩷(ลิงก์เข้าไลน์กดทางฟอร์มได้เลยค่า)"
        "<br><br>ไว้เจอกันนะ! ✨"
        "<br>ชมรมโลหิต จุฬาลงกรณ์มหาวิทยาลัย🩸"
    )


JOB = EmailJob(
    sheet_name=INTERVIEW_PASS_SHEET.sheet_name,
    start_row=INTERVIEW_PASS_SHEET.start_row,
    num_rows=INTERVIEW_PASS_SHEET.num_rows,
    start_col=INTERVIEW_PASS_SHEET.start_col,
    num_cols=INTERVIEW_PASS_SHEET.num_cols,
    subject=INTERVIEW_RESULT_SUBJECT,
    message_builder=get_message,
)


def main():
    run_email_job(JOB)


if __name__ == "__main__":
    main()
