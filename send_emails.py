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
SUBJECT = "Could You Please Help Me with a Backend Referral? "  
BODY_TEMPLATE = """\
Hi {name},

I hope you're doing well. I'm reaching out to explore potential Backend Developer opportunities at {company}.

I have 3 years of experience in backend development, specializing in microservices, cloud security UI, and storage solutions. At Juniper Networks, I contributed to cloud security and on-prem storage solutions, improving system efficiency and reliability.

I am actively looking for new opportunities and would love to discuss how my skills align with open roles at {company}. My expected base CTC is 25 LPA minimum. Please find my resume attached for your reference.

Would it be possible to schedule a quick call to discuss this further? You can reach me at +91 6303665574 at your convenience.

Looking forward to your response!

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
        msg.add_attachment(resume.read(), maintype="application", subtype="pdf", filename="Rakesh_Resume_Backened.pdf")

    try:
        server.send_message(msg)
        print(f"Email sent to {name} ({email})")
    except Exception as e:
        print(f"Failed to send email to {name} ({email}): {e}")

server.quit()
