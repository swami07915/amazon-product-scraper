from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import math
from selenium.webdriver.support.wait import WebDriverWait
import smtplib


ask=input("tell 3 key words about you words?\nfirst two should be must things\n1st key:")
ask2=input("2nd key:")
ask3=input("3rd key:")
ASK=ask.upper()
ASK2=ask2.upper()
ASK3=ask3.upper()
chrome_potions=webdriver.ChromeOptions()
chrome_potions.add_experimental_option("detach",True)
driver: Chrome=webdriver.Chrome(options=chrome_potions)
# from above here practice 3 4 times so you dont have to ask gpt



driver.get("https://www.amazon.in/ref=nav_logo")
driver.maximize_window()
time.sleep(4)
butten=driver.find_element(By.ID,"twotabsearchtextbox")
butten.send_keys(f"{ask} {ask2}",Keys.ENTER)


wait = WebDriverWait(driver, 10)
cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-component-type='s-search-result']")))
# you have to practice this line also

# ohh.click()
n=0
products=[]
while n<3:
    ohh = driver.find_element(By.CSS_SELECTOR, "a.s-pagination-next")
    cards=driver.find_elements(By.CSS_SELECTOR,"div[role='listitem']")
    print(cards)
    for card in cards:
        try:
            title = card.find_element(By.CSS_SELECTOR, "h2 span").text
            rating = float(card.find_element(By.CSS_SELECTOR, ".a-size-small.a-color-base").text)
            price=card.find_element(By.CLASS_NAME,"a-price-whole").text
            big_title = title.upper()
            rating_with_braket=card.find_element(By.CSS_SELECTOR, "a[href*='customerReviews'] span").text
            link=card.find_element(By.CSS_SELECTOR,"a[class^='a-link-normal']").get_attribute("href")
            rating_without=rating_with_braket.replace("(","").replace(")","")
            if "K" in rating_without:
                in_k=float(rating_without.replace("K",""))
                in_num=in_k*1000
                overall=rating*math.log10(in_num)
                overal=round(overall,2)
            else:
                overall=rating*math.log10(int(rating_without))
                overal=round(overall,2)


            # topfive=sorted(maxnum,reverse=True)[:5]
            if ASK in big_title and ASK2 in big_title and (ASK3 in big_title or ASK3 == ""):
                print(f"{title}={price} has rating={rating}----{overal}--score={overal}")
                products.append({
                    "score":overal,
                    "title":title,
                    "link":link
                })


        except Exception as e:
            pass
    n+=1
    ohh.click()
    wait.until(EC.staleness_of(cards[0]))

    time.sleep(2)
topfie=sorted(products,key=lambda x:x["score"],reverse=True)[:5]
print(topfie)

with smtplib.SMTP("smtp.gmail.com") as s:
    s.starttls()
    s.login(user="rudrakshdswami@gmail.com",password="passward")
    s.sendmail(
        from_addr="rudrakshdswami@gmail.com",
        to_addrs="rudrakshswami931@gmail.com",
        msg=f"your top 5 products\n\n{topfie}".encode("utf-8")
        )




