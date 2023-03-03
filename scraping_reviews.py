from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from math import floor
import pandas as pd

driver_path = './chromedriver.exe'

# URL de prueba
# url = 'https://www.google.com/maps/place/Escuela+T%C3%A9cnica+Superior+de+Ingenier%C3%ADa+Inform%C3%A1tica/@37.3582954,-5.9895639,17z/data=!3m1!4b1!4m6!3m5!1s0xd126dd4a3055555:0x29c3f634f8a021b8!8m2!3d37.3582954!4d-5.9873752!16s%2Fg%2F121yb2tm'
# url = 'https://www.google.com/maps/place/Victoria+and+Albert+Museum/@51.4966392,-0.17218,15z/data=!4m5!3m4!1s0x0:0x9eb7094dfdcd651f!8m2!3d51.4966392!4d-0.17218'
# url = 'https://www.google.com/maps/place/Universidad+de+Sevilla+Facultad+de+Matem%C3%A1ticas/@37.3593497,-5.9902154,17z/data=!4m6!3m5!1s0xd126dd35d59d14f:0x8e628875e7ac28cd!8m2!3d37.3593497!4d-5.9880267!16s%2Fg%2F1q5bp3qmf'
# url = 'https://www.google.com/maps/place/H%26M/@40.7560149,-73.9882323,17z/data=!3m1!5s0x89c258fe5ddfa089:0xeaee31cfd3c3b84c!4m6!3m5!1s0x89c25854d7f642fd:0x92c6f656266909f!8m2!3d40.7560149!4d-73.9860436!16s%2Fg%2F1yh9tfdx_?hl=en'


# H&M London UK, The Arcade, London E20 1EL, United Kingdom
# url = 'https://www.google.com/maps/place/H%26M/@51.5430288,-0.0065102,17z/data=!3m1!4b1!4m6!3m5!1s0x48761d64764cc48f:0x2810ae4e5bbca0e2!8m2!3d51.5430288!4d-0.0043215!16s%2Fg%2F12hp0k6kq?hl=en'
# csv_path = 'google_reviews_london.csv'
# H&M London UK, 224 Regent St., London W1B 3BR, United Kingdom
url ='https://www.google.com/maps/place/H%26M/@51.5140976,-0.1432836,17z/data=!3m2!4b1!5s0x4876052b665811cb:0x7e5657d0fabeb4f0!4m6!3m5!1s0x4876052aa7f7d857:0xbe912c31c77ef6b8!8m2!3d51.5140976!4d-0.1410949!16s%2Fg%2F1tdz49pz?hl=en'
csv_path = 'google_reviews_london2.csv'
# H&M Lakeland USA, 3800 US Hwy 98 N, Lakeland, FL 33809, United States
# url = 'https://www.google.com/maps/place/H%26M/@28.0904932,-81.9781633,17z/data=!3m1!4b1!4m6!3m5!1s0x88dd47145f5524ad:0x15511fa0ae8180f2!8m2!3d28.0904932!4d-81.9781633!16s%2Fm%2F0406n0c?authuser=0&hl=en'
# csv_path = 'google_reviews_lakeland.csv'
# H&M Boston USA, 100 Newbury St, Boston, MA 02116, United States
# url = 'https://www.google.com/maps/place/H%26M+HOME/@42.3513545,-71.0752124,17z/data=!3m1!4b1!4m6!3m5!1s0x89e3708370927693:0x22c5e58db8bba597!8m2!3d42.3513545!4d-71.0752124!16s%2Fg%2F1v7tmcxn?authuser=0&hl=en'
# csv_path = 'google_reviews_boston.csv'


def connect(driver_path, url):
    # Habilitar driver
    options = webdriver.ChromeOptions()
    s = Service(driver_path)
    driver = webdriver.Chrome(service=s, options=options)
    # Acceder a URL
    driver.get(url)
    # Habilitar cookies
    try:
        driver.find_element('xpath', '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button').click()
        # time.sleep(3)
    except Exception as e:
        print("Error de aceptacion de cookies (quiza las cookies ya esten aceptadas)")
        print(e)
    return driver


def load_reviews(driver, file_name):
    # Numero de reviews totales
    snumber_reviews = driver.find_element('xpath', '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[2]/span[1]/span').text.split(" ")[0]
    number_reviews = int(snumber_reviews.replace(",",""))
    print(number_reviews)
    
    # Cargar todas las reviews
    try:
        reviews_button = driver.find_element('xpath','//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]')
        reviews_button.click()
        time.sleep(3)    
    except Exception as e:
        print("Error: no se encuentra botón de ampliar reseñas (puede que haya pocas reseñas)")
        print(e)

    # Scrollear las noticias
    try:
        sort_div = driver.find_element('xpath','//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[8]/div[2]/button')
        sort_div.click()
        sort_recientes = driver.find_element('xpath','//*[@id="action-menu"]/div[2]')
        sort_recientes.click()
    except Exception as e:
        print("Error: no se pueden ordenar las noticias")

    last_height = driver.execute_script("return document.body.scrollHeight")
    number_scrolls = 0
    
    while True: # number_scrolls < floor(number_reviews/10):

        number_scrolls = number_scrolls+1
    
        scroll_div = driver.find_element('xpath', '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')
        # driver.execute_script('arguments[0].scrollBy(0, 5000);', scroll_div)
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scroll_div)

        time.sleep(3)

        scroll_div = driver.find_element('xpath', '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')
        new_height = driver.execute_script("return document.body.scrollHeight", scroll_div)

        div = driver.find_elements('xpath', '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[10]')[0]
        noticias = len(div.find_elements(By.CLASS_NAME, 'rsqaWe'))

        print(number_scrolls, noticias)

        if noticias == number_reviews or noticias >1100:
            break

        # if new_height == last_height and number_scrolls>1:
        #     break

        # last_height = new_height
    
    # Extraer informacion
    div = driver.find_elements('xpath', '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[10]')[0]
    time.sleep(3)

    names_list = []
    stars_list = []
    reviews_list = []
    dates_list = []

    
    buttons = div.find_elements(By.TAG_NAME, 'button') 
    for msg in buttons:
        if msg.text == 'More':
            msg.click()
            # print("CLICKEADO")
    time.sleep(3)

    dates = div.find_elements(By.CLASS_NAME, 'rsqaWe')
    names = div.find_elements(By.CLASS_NAME, 'd4r55')
    stars = div.find_elements(By.CLASS_NAME, 'kvMYJc')
    reviews = div.find_elements(By.CLASS_NAME, 'wiI7pd')

    print(len(dates))
    
    for date, name, star, review in zip(dates, names, stars, reviews):
        dates_list.append(date.text)
        stars_list.append(star.get_attribute("aria-label").strip()[0])
        reviews_list.append(review.text.replace('\n',' '))
        names_list.append(name.find_element(By.TAG_NAME, 'span').text)
    
    review = pd.DataFrame(
        {
        'date': dates_list,
        'user_name': names_list,
        'review': reviews_list, 
        'star': stars_list
        }
    )

    review.to_csv(file_name,index=False,sep='|')


    print(review.head())




def main():
    driver = connect(driver_path, url)
    load_reviews(driver, csv_path)
    while True:
        pass



if __name__ == "__main__":
    main()