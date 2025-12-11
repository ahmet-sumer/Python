import smtplib, ssl
import pandas as pd
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import base64



#^ ============= Info Part ================

sender_email = "your@mail.com"
receiver_email = "receiver@email.com"
password = "Password"
smtp_server = "smtp.yandex.com" # or "smtp.gmail.com"
port = 465
csv_file = "sample.csv"
log_file = "sent_email.csv"
mail_per_day = 3
WEBSITE = "https://www.yourwebsite.com.tr"
ITEMS_PER_PAGE = 10

#* ====================================

def load_data():
    try:
        df = pd.read_csv(csv_file)
        print(f"{len(df)} dataset loaded orrectly!")
        return df
    except FileNotFoundError:
        print("Could'nt load the CSV file")
        return None
    
def display_recipient_paginated(df, page=0):
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    page_df = df.iloc[start:end]
    total_pages = (len(df) + ITEMS_PER_PAGE - 1 ) // ITEMS_PER_PAGE

    print("=" * 50)
    print(f"Sender List (Page {page+1}/{total_pages}) - Total Reciepents {len(df)}")
    print("=" * 50)

    for idx, row in page_df.iterrows():
        print(f"\n{idx}   {row["Brand-name"]}")
        print(f" Website: {row["Website"]}")
        print(f" Email:   {row["E-mail"]}")
        print(f" Address: {row["Address"]}")
    print("=" * 50)


    nav_text = f"Page {page+1}/{total_pages} -"
    if page > 0:
        nav_text += " [p/Previous] "
    elif page < total_pages - 1:
        nav_text += " [n/Next] "
    else:
        nav_text += " [(0-10) Pick One] "


    print(nav_text)
    return page, total_pages


def get_user_selection(df):
    
    page = 0
    total_pages = 0

    while True:
        page, total_pages = display_recipient_paginated(df, page)

        choise = input("\n What is your choise").strip().lower()

        if choise == "p":
            if page > 0:
                page -= 1
            else:
                print("It's Already first Page")
            continue
            
        elif choise == "n":
            if page < total_pages - 1:
                page += 1
            else:
                print("It's Already Last Page")
            continue

        else:
            try:
                page_idx = int(choise)

                start = page * ITEMS_PER_PAGE
                real_idx = start + page_idx

                if page_idx < 0 or page_idx >= ITEMS_PER_PAGE:
                    print(f"There is no {page_idx}. item here/ Choose between 0-9")
                    continue
                if real_idx > len(df):
                    print(f"You passed the length of your CSV file try again between 0-{len(df)}")
                    continue

                selected = df.iloc[real_idx]

                sender_name = input("Enter your sender name: ") 

                if not sender_name:
                    print("You can't left empty sender name") 
                    continue

                print("\n Summary")
                print(f" Sender: {sender_email}")
                print(f" Reciever=>  Email:{selected['email']} Brand Name:{selected['brand-name']}")
                print(" This Recipient will deleted after sending email")

                confirm = input("Do you want to send the e-mail now?(y/n): ").lower()

                if confirm == "y":
                    return selected, sender_name, real_idx
            

            except Exception as e:
                print(f"There was {e} issue. Try again")
    

def send_email(recipient, sender_name, attachment_path=None, logo_path=None):
    receiver_email = recipient['email']

    subject = "" #TODO Subject of your mail

    logo_html = ""
    if logo_path and os.path.exists(logo_path):
        with open (logo_path, "rb",) as f:
            logo_data = base64.b64encode(f.read()).decode()
        logo_ext = logo_path.split('.')[-1]
        logo_html = f'<img src="data:image/{logo_ext};base64,{logo_data}",width="150px"><br><br>'


    body = ""#TODO Body Message of your mail

    #* MIME Message Part

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    part = MIMEText(body,'html','utf-8')
    msg.attach(part)

    if attachment_path and os.path.exists(attachment_path):
        with open (attachment_path, 'rb') as attachment:
            part = MIMEBase('application','octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
            msg.attach(part)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email,password)
            server.sendmail(sender_email, receiver_email, msg.as_string())

    except Exception as e:
        print(f"There was {e} issue. Try Again")


def log_email_to_history(recipient, sender_name, status):
    log_data= {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'time': datetime.now().strftime('%H-%M'),
        'sender_name': sender_name,
        'receiver_brand': recipient['brand_name'], 
        'receiver_mail': recipient['email'],
        'status': status
    }

    if os.path.exists(log_file):
        df = pd.read_csv(log_file)
        df = pd.concat([df, pd.DataFrame([log_data])], ignore_index=True)
    else:
        df = pd.DataFrame([log_data])
    
    df.to_csv(log_file, index=False, encoding='utf-8-sig')
    print("Your file has been saved") 

def remove_from_csv(df,idx):
    df = df.drop(idx)
    df.reset_index(drop=True, inplace=True)
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    print(f"Removed from CSV file. {len(df)} Recipient has been left")
    return df


def check_daily_limit():

    if not os.path.exists(log_file):
        return True

    df = pd.read_csv(log_file)
    today = datetime.now().strftime('%Y-%m-%d')
    today_emails = len(df[df['date'] == today])

    if today_emails >= mail_per_day:
        print("You've sent your e-mails for today take a rest and get back here tomorrow.")
        print(f"By the way you have total of {mail_per_day} emails per day")
        return False
    else:
        remaining = mail_per_day - today_emails
        print(f"You have {remaining} emails to sent today")
        return True


def main():
    print("=" * 50)
    print("Welcome to email send system")
    print("=" * 50)

    if not check_daily_limit():
        return

    df = load_data()
    if df is None:
        return

    selected_recipient, sender_name, idx = get_user_selection(df)
    success = send_email(
        selected_recipient,
        sender_name,
        attachment_path="",
        logo_path=""
    )
    if success:
        log_email_to_history(selected_recipient,sender_name, 'Sent')

        df = remove_from_csv(df, idx)

        again = input("Do you want to send email to someone else?(y/n): ")
        if again == "y":
            main()
        else:
            print("Bye")

    else:
        print("Could'nt Send and remove the email")




if __name__ == '__main__':
    main()