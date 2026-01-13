import smtplib

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart
 
# 使用本地 MTA，不需要指定外部 smtp_server

smtp_server = "localhost"

smtp_port = 25  # 本地 MTA 通常监听 25 端口
 
sender_email = "yong.xiong@nxp.com"

receiver_email = "yong.xiong@nxp.com"
 
subject = "SMTP Relay Test"

body = "Hello, this is a test email sent via local MTA without calling sendmail."
 
# 构建邮件

msg = MIMEMultipart()

msg["From"] = sender_email

msg["To"] = receiver_email

msg["Subject"] = subject

msg.attach(MIMEText(body, "plain"))
 
try:

    with smtplib.SMTP(smtp_server, smtp_port) as server:

        server.sendmail(sender_email, receiver_email, msg.as_string())

    print(f"邮件发送成功！")

except Exception as e:

    print(f"邮件发送失败: {e}")
 