import smtplib
import os
import pandas as pd
from email.message import EmailMessage

# Fetch credentials from GitHub Secrets
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Read Excel file
df = pd.read_excel("hr_contacts_test.xlsx")

# Email content
SUBJECT = "Hey {name}, Could You Help Me with a Backend Opportunity?"
BODY_TEMPLATE = """\
Dear {name},

I hope you're doing well. I'm reaching out to explore any job opportunities at {company} for a Backend Developer role.

I have 3 years of experience in backend development, including microservices, cloud security UI, and storage solutions. I previously worked at Juniper Networks, where I contributed to cloud security and on-prem storage solutions.

I am actively looking for new opportunities, and I would love to discuss how my experience aligns with any open roles at {company}. Please find my resume attached for your reference.

Would it be possible to schedule a quick call? You can reach me at +91 6303665574 at your convenience.

Looking forward to hearing from you!

Best regards,
Rakesh Peddamallu
+91 6303665574 
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
