from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import random
import smtplib
import ssl
from email.message import EmailMessage

# Initializing webpage interaction variables.
PATH = "Path to chromedriver.exe. For example, D:\chromedriver.exe"
driver = webdriver.Chrome(PATH)
max_wait = 6

# Initializing email sending.
# Disclaimer: You are going to need to set up your own email account to send yourself a notification.
port = 465
password = "Sender email password"
context = ssl.create_default_context()
msg = EmailMessage()
msg["Subject"] = "ATC Alert"
msg["From"] = "Sender email address"
msg["To"] = "Receiving email address"

# Opening product webpage. Example: https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440
driver.get("Product Webpage")

in_stock = False
while not in_stock:
    try:
        # Checking if item is sold out.
        atc_button = WebDriverWait(driver, 0.25).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn-disabled"))
        )
        print("Item is sold out. Refreshing.")
        time.sleep(random.randint(1, max_wait))
        driver.refresh()

    except:
        # Clicking add to cart button.
        print("Item is in stock. Adding to cart.")
        atc_button = driver.find_element_by_class_name("btn-primary")
        atc_button.click()
        in_stock = True

# Email Alert
with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(msg["From"], password)
    server.send_message(msg)
