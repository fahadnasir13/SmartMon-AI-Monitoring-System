import yagmail

def send_alert(subject, body):
    sender_email = "2021bbit15@student.uet.edu.pk"
    app_password = "  "  # Not your Gmail password!

    receiver = "2021bbit15@student.uet.edu.pk"  # Can be same or someone else

    try:
        yag = yagmail.SMTP(sender_email, app_password)
        yag.send(to=receiver, subject=subject, contents=body)
        print("✅ Alert email sent!")
    except Exception as e:
        print("❌ Failed to send email:", e)
