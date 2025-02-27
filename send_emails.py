import smtplib
import os
import pandas as pd
from email.message import EmailMessage

# Fetch credentials from GitHub Secrets
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Read Excel file
df = pd.read_excel("hr_contacts.xlsx")

# Email content
SUBJECT = "Looking for Job Opportunities - Backend Developer"
BODY_TEMPLATE = """\
Dear {name},

I hope you're doing well. I am reaching out to explore any job opportunities at {company} for a Backend Developer role.

I have 2.5 years of experience in backend development, working with microservices, cloud security UI, and storage solutions. Please find my resume attached.

Looking forward to hearing from you.

Best regards,  
Rakesh Peddamallu  
+91 XXXXXXXXXX  
"""

# Set up SMTP server
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

# Send emails
for _, row in df.iterrows():
    name, email, company = row["Name"], row["Email"], row["Company"]

    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = email
    msg["Subject"] = SUBJECT
    msg.set_content(BODY_TEMPLATE.format(name=name, company=company))

    # Attach resume
    with open("resume.pdf", "rb") as resume:
        msg.add_attachment(resume.read(), maintype="application", subtype="pdf", filename="Rakesh_Resume.pdf")

    try:
        server.send_message(msg)
        print(f"Email sent to {name} ({email})")
    except Exception as e:
        print(f"Failed to send email to {name} ({email}): {e}")

server.quit()
