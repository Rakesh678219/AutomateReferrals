import smtplib
import os
import pandas as pd
from email.message import EmailMessage
from time import sleep

# Fetch credentials from environment variables
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    raise ValueError("Email credentials are not set in environment variables.")

# Read Excel file
try:
    df = pd.read_excel("hr_contacts.xlsx")
except FileNotFoundError:
    raise FileNotFoundError("The 'hr_contacts.xlsx' file was not found.")

# Email content
SUBJECT = "Could You Please Help Me with a Backend Referral?"  
BODY_TEMPLATE = """\
Hi {name},

I hope you're doing well. My name is Rakesh Peddamallu, and I'm reaching out to explore potential Backend Developer opportunities at {company}.

I have 3 years of experience in backend development, specializing in microservices, cloud security UI, and storage solutions. At Juniper Networks, I contributed to cloud security and on-prem storage solutions, improving system efficiency and reliability.

I am actively looking for new opportunities and would love to discuss how my skills align with open roles at {company}. My expected base salary is 25 LPA and open for negotiation. Please find my resume attached for your reference.

Would it be possible to schedule a quick call to discuss this further? You can reach me at +91 6303665574 at your convenience.

Looking forward to your response!

Best regards,  
Rakesh Peddamallu  
+91 6303665574
"""

# Check if resume exists
resume_path = "resume.pdf"
if not os.path.exists(resume_path):
    raise FileNotFoundError(f"The resume file '{resume_path}' was not found.")

# Send emails using SMTP
def send_email(name, email, company):
    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = email
    msg["Subject"] = SUBJECT
    msg.set_content(BODY_TEMPLATE.format(name=name, company=company))

    # Attach resume
    with open(resume_path, "rb") as resume:
        msg.add_attachment(resume.read(), maintype="application", subtype="pdf", filename="Rakesh_Resume_Backend.pdf")
    
    return msg

# SMTP Connection
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        for _, row in df.iterrows():
            name, email, company = row["Name"], row["Email"], row["Company"]
            msg = send_email(name, email, company)

            # Retry mechanism for transient errors
            for attempt in range(3):
                try:
                    server.send_message(msg)
                    print(f"✅ Email sent to {name} ({email})")
                    break
                except smtplib.SMTPException as e:
                    print(f"⚠️ Attempt {attempt + 1} failed for {email}: {e}")
                    sleep(2)  # Wait before retrying
                except Exception as e:
                    print(f"❌ Failed to send email to {name} ({email}): {e}")
                    break

except smtplib.SMTPAuthenticationError:
    print("❌ Authentication failed. Check your email and password.")
except smtplib.SMTPConnectError:
    print("❌ Failed to connect to the SMTP server.")
except Exception as e:
    print(f"❌ An unexpected error occurred: {e}")
