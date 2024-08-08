import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_flats(url, budget):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    flat_list = soup.find_all("a", class_="property")
    filtered_flats = []

    for flat in flat_list:
        flat_url = flat.get("href")
        price_elem = flat.find("span", class_="price__amount")
        building_elem = flat.find("span", class_="property__name")
        area_elem = flat.find("span", class_="property__address")
        
        if price_elem and building_elem and area_elem:
            price = float(price_elem.text.strip().replace(",", ""))
            building = building_elem.text.strip()
            area = area_elem.text.strip()
            flat_url = "https://www.theblueground.com" + flat_url
            
            if price < budget:
                filtered_flats.append({
                    "url": flat_url,
                    "area": area,
                    "building": building,
                    "price": price,
                })
    
    return filtered_flats

def send_email(sender_email, sender_password, recipient_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

def main():
    url = "https://www.theblueground.com/furnished-apartments-dubai-uae"
    budget = 6000
    
    flats = get_flats(url, budget)
    
    if flats:
        email_body = "Flats within your budget:\n\n"
        for flat in flats:
            email_body += f"Area: {flat['area']}\n"
            email_body += f"Building: {flat['building']}\n"
            email_body += f"Price: {flat['price']}\n"
            email_body += f"URL: {flat['url']}\n\n"
        
        sender_email = "your_email@gmail.com"
        sender_password = "your_password"
        recipient_email = "recipient@example.com"
        subject = "Blueground Flats Within Your Budget"
        
        send_email(sender_email, sender_password, recipient_email, subject, email_body)
    else:
        print("No flats found within the specified budget.")

if __name__ == "__main__":
    main()