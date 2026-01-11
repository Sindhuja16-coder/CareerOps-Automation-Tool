import smtplib
import schedule
import time
import feedparser
import sys
import urllib.parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==============================================================================
#  🛠️ USER SETTINGS (EDIT THIS SECTION ONLY)
# ==============================================================================

# 1. EMAIL SETUP
MY_EMAIL = "ENTER_YOUR_EMAIL@gmail.com"
MY_PASSWORD = "ENTER_YOUR_APP_PASSWORD"

# 2. JOB PREFERENCES
# Change this to your target city (e.g., "Bangalore", "Mumbai", "Remote")
TARGET_CITY = "Hyderabad"

# Add the job titles you want to find inside the brackets [ ]
# Make sure each title is inside quotes " " and separated by a comma.
TARGET_ROLES = ["Data Analyst", "Data Engineer", "Python Developer"]

# 3. EXPERIENCE FILTER
# If you are a fresher/junior (0-3 years), keep these words to BLOCK senior roles.
# If you WANT senior roles, just make this list empty like: AVOID_KEYWORDS = []
AVOID_KEYWORDS = ["Senior", "Sr.", "Lead", "Manager", "Director", "Head", "Principal", "Architect"]

# ==============================================================================
#  ✅ DONE. DO NOT TOUCH ANYTHING BELOW THIS LINE.
#  (The bot will do the rest of the magic automatically!)
# ==============================================================================

# --- SAFETY CHECK: Did the user update the email? ---
if "ENTER_YOUR" in MY_EMAIL:
    print("\n" + "!"*60)
    print("❌ SETUP ERROR: You forgot to add your Email!")
    print("   Please open 'job_alerts.py' and edit the USER SETTINGS section.")
    print("!"*60 + "\n")
    input("Press Enter to exit...")
    sys.exit()

def fetch_jobs():
    print(f"🔎 Searching for {TARGET_ROLES} jobs in {TARGET_CITY}...")
    
    found_jobs = []
    
    # --- AUTOMATIC LINK GENERATOR ---
    # This loop creates Google RSS links for exactly what the user asked for.
    for role in TARGET_ROLES:
        # We safely encode the text (e.g. "Data Analyst" becomes "Data+Analyst")
        query = f"{role} jobs {TARGET_CITY}"
        encoded_query = urllib.parse.quote(query)
        
        # Build the dynamic URL
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}+when:1d&hl=en-IN&gl=IN&ceid=IN:en"
        
        feed = feedparser.parse(rss_url)
        
        for entry in feed.entries:
            title = entry.title
            link = entry.link
            
            # 1. Filter: Remove "Senior/Lead" roles if the user requested
            if not any(bad.lower() in title.lower() for bad in AVOID_KEYWORDS):
                
                # Clean up title
                clean_title = title.split(" - ")[0]
                job_entry = f"📍 {clean_title}\n🔗 {link}\n"
                
                if job_entry not in found_jobs:
                    found_jobs.append(job_entry)

    if found_jobs:
        print(f"✅ Found {len(found_jobs)} new jobs! Sending email...")
        send_email(found_jobs[:15]) # Send top 15 results
    else:
        print("😴 No new relevant jobs found right now.")

def send_email(job_list):
    msg = MIMEMultipart()
    msg['From'] = MY_EMAIL
    msg['To'] = MY_EMAIL
    msg['Subject'] = f"🚀 {TARGET_CITY} Job Alert: {len(job_list)} New Roles"

    body = f"Here are the latest jobs for {TARGET_ROLES} in {TARGET_CITY}:\n\n" + "\n".join(job_list)
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(MY_EMAIL, MY_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("📧 Email sent successfully!")
    except Exception as e:
        print("\n" + "❌ LOGIN ERROR: Could not log in to Gmail.")
        print("   Check your App Password and Email in the User Settings.")
        print(f"   Error: {e}\n")

# --- SCHEDULER ---
print("⏳ Job Alert Service Started...")
print(f"   Target: {TARGET_ROLES} in {TARGET_CITY}")
print("   Checking now...")
fetch_jobs() # Run once immediately

# Schedule to run twice a day
schedule.every().day.at("10:00").do(fetch_jobs)
schedule.every().day.at("18:00").do(fetch_jobs)

while True:
    schedule.run_pending()
    time.sleep(60)