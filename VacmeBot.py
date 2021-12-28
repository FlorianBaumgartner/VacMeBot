import time
import telegram_send
# from pynput import keyboard
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime


url = "https://boostli.web.app/"
date_threshold = "04.01.2022"
target_location = "Impfzentrum MEDIN Biel – mRNA"
sleep_time = 60


telegram_send.send(messages=["Start Program"])
date_threshold = datetime.strptime(date_threshold, '%d.%m.%Y')
# listener = keyboard.Listener(on_press=lambda x: globals().update(run=False))
# listener.start()
oldDate = None
run = True

while(run):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("headless")    # Open browser in background
        driver = webdriver.Chrome(ChromeDriverManager().install(),
                                  chrome_options=options)
        driver.get(url)
        time.sleep(1)     # Give some time to fully load content
        
        locations = driver.find_elements_by_class_name("ng-star-inserted")
        content = [location.text for location in locations]
        driver.quit()
        
        index = content.index(target_location)
        loc = content[index - 1].splitlines()
        date = datetime.strptime(",".join(loc[1].split(", ")[1:]), '%B %d,%Y')
        print(f"\n\nWebsite updated: {date.strftime('%d.%m.%Y')}")
        
        if(oldDate != date):
            oldDate = date
            print("This is the first time we have seen this new date")
            if(date < date_threshold):
                print("We have found an appointment within threshold!")
                message = (f"Appointment available: {date.strftime('%d.%m.%Y')}\n"
                           "Visit now https://be.vacme.ch/start\n"
                           "Good Luck!")
                telegram_send.send(messages=[message])
    
    except Exception as e:
        print(f"Exception occured: {e}")
        
    now = time.time()
    while(time.time() - now < sleep_time):
        time.sleep(0.1)
        if(not run):
            break


print("Terminate Program")
telegram_send.send(messages=["Terminate Program"])
