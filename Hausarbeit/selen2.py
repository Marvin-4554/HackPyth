import os
import shutil
import stat
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

s = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=s)

download_path = 'downloaded_code'
websites = ["https://github.com/Timm4J/HackPyth", "https://github.com/Marvin-4554/HackPyth"]
for website in websites:
    driver.get(website)

    if os.path.exists(download_path):
        shutil.rmtree(download_path)
    else:
        os.makedirs(download_path)

    git_process = subprocess.run(["git", "clone", "--single-branch", "--branch", "main", website, download_path], capture_output=True, text=True)

    prospector_process = subprocess.Popen(["prospector", "-w", "bandit", download_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    prospector_output, prospector_error = prospector_process.communicate()
    
    print(prospector_output)
               

    # Setzen von Schreibrecht auf den Ordner, um ihn löschen zu können
    if os.path.exists(download_path):
        for root, dirs, files in os.walk(download_path):
            for name in files:
                os.chmod(os.path.join(root, name), stat.S_IWUSR)  # Setze Schreibrechte für den Benutzer
            for name in dirs:
                os.chmod(os.path.join(root, name), stat.S_IWUSR)  # Setze Schreibrechte für den Benutzer
        shutil.rmtree(download_path)

driver.quit


"""
title = ""
key = ""

for i in range(1, 10):
    try:
        title = driver.find_element(By.XPATH, '//*[@id="LC' + str(i) + '"]').text
        if "SECRET_KEY" in title:
            print(f"Found the secret key in line {i}")
            key = title.split(" ")[2].replace("'", "")
            break
    except:
        pass


key = driver.find_element(By.XPATH, "//textarea[contains(text(), 'SECRET_KEY')" + "]").text

key = key.split("\n")

for i in key:
    if "SECRET_KEY" in i:
        key = i.split(" ")[2].replace("'", "")
        break

print("Gefundener Secret Key: ", key)

with open("secret_key.txt", "w") as file:
    file.write(key)

driver.quit()
"""