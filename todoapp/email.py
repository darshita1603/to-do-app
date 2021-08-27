def send_email(pdf):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    import smtplib
    from email.mime.application import MIMEApplication


    #The mail addresses and password
    sender_address = 'darshitactridhyatech@gmail.com'
    sender_pass = 'Tridhya@2345'
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = pdf.user.email
    message['Subject'] = f'[darshita] {pdf.user.username} Your task History!!!'
    #The subject line
    message.attach(MIMEText(f"Task Name :{pdf.name_of_task}", "plain"))
    with open("media/pdf_files/task_history_pdf.pdf", "rb") as f:
        attach = MIMEApplication(f.read(),_subtype="pdf")
        attach.add_header('Content-Disposition','attachment',filename=str("media/pdf_files/task_history_pdf.pdf"))
        message.attach(attach)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_address, sender_pass)
    server.send_message(message)
    server.quit()