import time
import telegram_send
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime


url = "https://boostli.web.app/"
date_threshold = "04.01.2022"
target_location = "Impfzentrum MEDIN Biel – mRNA"
sleep_time = 40


telegram_send.send(messages=["Start Program"])
date_threshold = datetime.strptime(date_threshold, '%d.%m.%Y')
oldDate = None

while(True):
    now = time.time()
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("headless")    # Open browser in background
        driver = webdriver.Chrome(ChromeDriverManager().install(),
                                  chrome_options=options)
        driver.get(url)
        time.sleep(2.5)     # Give some time to fully load content
        
        locations = driver.find_elements_by_class_name("ng-star-inserted")
        content = [location.text for location in locations]
        driver.quit()
        
        index = content.index(target_location)
        loc = content[index - 1].splitlines()
        date = datetime.strptime(",".join(loc[1].split(", ")[1:]), '%B %d,%Y')
        print(f"\n\nWebsite updated: {date.strftime('%d.%m.%Y')}")
        
        with open("log.csv", 'a+') as f:
            f.write(f"{time.time()};{date.strftime('%d.%m.%Y')}\n")
        
        if(oldDate != date):
            oldDate = date
            print("This is the first time we have seen this date")
            if(date < date_threshold):
                print("We have found an appointment within threshold!")
                ms = (f"Appointment available: {date.strftime('%d.%m.%Y')}\n"
                       "Visit now https://be.vacme.ch/start\n"
                       "Good Luck!")
                telegram_send.send(messages=[ms])
    
    except Exception as e:
        print(f"Exception occured: {e}")
        
    time.sleep(max(0, sleep_time - (time.time() - now)))


print("Terminate Program")
telegram_send.send(messages=["Terminate Program"])
