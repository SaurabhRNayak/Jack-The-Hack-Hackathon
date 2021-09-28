from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
class WebDriver:

    location_data = {}

    def __init__(self):
        self.PATH = "chromedriver.exe"
        self.options = Options()
        self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(self.PATH, options=self.options)

        self.location_data["stay"] = "NA"
        self.location_data["rating"] = "NA"
        self.location_data["reviews_count"] = "NA"
        self.location_data["location"] = "NA"
        self.location_data["contact"] = "NA"
        self.location_data["website"] = "NA"
        self.location_data["checkin_time"] = "NA"
        self.location_data["checkout_time"] = "NA"
        # self.location_data["Time"] = {"Monday":"NA", "Tuesday":"NA", "Wednesday":"NA", "Thursday":"NA", "Friday":"NA", "Saturday":"NA", "Sunday":"NA"}
        # self.location_data["Reviews"] = []
        # self.location_data["Popular Times"] = {"Monday":[], "Tuesday":[], "Wednesday":[], "Thursday":[], "Friday":[], "Saturday":[], "Sunday":[]}

    def click_open_close_time(self):

        if(len(list(self.driver.find_elements_by_class_name("cX2WmPgCkHi__section-info-hour-text")))!=0):
            element = self.driver.find_element_by_class_name("cX2WmPgCkHi__section-info-hour-text")
            self.driver.implicitly_wait(5)
            ActionChains(self.driver).move_to_element(element).click(element).perform()

    def click_all_reviews_button(self):

        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "allxGeDnJMl__button")))

            element = self.driver.find_element_by_class_name("allxGeDnJMl__button")
            element.click()
        except:
            self.driver.quit()
            return False

        return True

    def get_location_data(self):

        try:
            stay=self.driver.find_element_by_xpath("""//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1/span[1]""")
            avg_rating = self.driver.find_element_by_class_name("gm2-display-2")
            total_reviews = self.driver.find_element_by_xpath("""//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/span[1]/span/span[1]/span[2]/span[1]/button""")
            address = self.driver.find_element_by_xpath("""//*[@id="pane"]/div/div[1]/div/div/div[18]/div[1]/button/div[1]/div[2]/div[1]""")
            phone_number = self.driver.find_element_by_xpath("""//*[@id="pane"]/div/div[1]/div/div/div[18]/div[4]/button/div[1]/div[2]/div[1]""")
            website = self.driver.find_element_by_xpath("""//*[@id="pane"]/div/div[1]/div/div/div[18]/div[3]/button/div[1]/div[2]/div[1]""")
            checkin_time= self.driver.find_element_by_xpath("""//*[@id="pane"]/div/div[1]/div/div/div[18]/div[6]/div[1]/div[2]/div[2]/span[1]""")
            checkout_time= self.driver.find_element_by_xpath("""//*[@id="pane"]/div/div[1]/div/div/div[18]/div[6]/div[1]/div[2]/div[2]/span[2]""")
        except:
            pass
        try:
            self.location_data["stay"] = stay.text
            self.location_data["rating"] = avg_rating.text
            self.location_data["reviews_count"] = total_reviews.text
            self.location_data["location"] = address.text
            self.location_data["contact"] = phone_number.text
            self.location_data["website"] = website.text
            self.location_data["checkin_time"] = checkin_time.text
            self.location_data["checkout_time"] = checkout_time.text
        except:
            pass


    def get_location_open_close_time(self):

        try:
            days = self.driver.find_elements_by_class_name("lo7U087hsMA__row-header")
            times = self.driver.find_elements_by_class_name("lo7U087hsMA__row-interval")

            day = [a.text for a in days]
            open_close_time = [a.text for a in times]

            for i, j in zip(day, open_close_time):
            	self.location_data["Time"][i] = j
		
        except:
            pass

    def get_popular_times(self):
        try:
            a = self.driver.find_elements_by_class_name("section-popular-times-graph")
            dic = {0:"Sunday", 1:"Monday", 2:"Tuesday", 3:"Wednesday", 4:"Thursday", 5:"Friday", 6:"Saturday"}
            l = {"Sunday":[], "Monday":[], "Tuesday":[], "Wednesday":[], "Thursday":[], "Friday":[], "Saturday":[]}
            count = 0

            for i in a:
                b = i.find_elements_by_class_name("section-popular-times-bar")
                for j in b:
                    x = j.get_attribute("aria-label")
                    l[dic[count]].append(x)
                count = count + 1

            for i, j in l.items():
                self.location_data["Popular Times"][i] = j
        except:
	        pass

    def scroll_the_page(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "section-layout-root")))
            pause_time = 2
            max_count = 5
            x = 0

            while(x<max_count):
                scrollable_div = self.driver.find_element_by_css_selector('div.section-layout.section-scrollbox.scrollable-y.scrollable-show')
                try:
                    self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
                except:
                    pass
                time.sleep(pause_time)
                x=x+1
        except:
            self.driver.quit()

    def expand_all_reviews(self):
        try:
            element = self.driver.find_elements_by_class_name("section-expand-review")
            for i in element:
                i.click()
        except:
            pass

    def get_reviews_data(self):
        try:
            review_names = self.driver.find_elements_by_class_name("section-review-title")
            review_text = self.driver.find_elements_by_class_name("section-review-review-content")
            review_dates = self.driver.find_elements_by_css_selector("[class='section-review-publish-date']")
            review_stars = self.driver.find_elements_by_css_selector("[class='section-review-stars']")

            review_stars_final = []

            for i in review_stars:
                review_stars_final.append(i.get_attribute("aria-label"))

            review_names_list = [a.text for a in review_names]
            review_text_list = [a.text for a in review_text]
            review_dates_list = [a.text for a in review_dates]
            review_stars_list = [a for a in review_stars_final]

            for (a,b,c,d) in zip(review_names_list, review_text_list, review_dates_list, review_stars_list):
                self.location_data["Reviews"].append({"name":a, "review":b, "date":c, "rating":d})

        except Exception as e:
            pass

    def scrape(self, url):
        try:
            self.driver.get(url)
        except Exception as e:
            self.driver.quit()
            # continue
        time.sleep(10)

        # self.click_open_close_time()
        self.get_location_data()
        # self.get_location_open_close_time()
        # self.get_popular_times()

        if(self.click_all_reviews_button()==False):
            # continue
                    pass

        time.sleep(5)
        self.scroll_the_page()
        self.expand_all_reviews()
        self.get_reviews_data()
        self.driver.quit()

        return(self.location_data)

urls = ["https://www.google.co.in/maps/place/ibis+Kochi+City+Centre/@9.9862365,76.2829359,15.33z/data=!4m18!1m9!2m8!1sHotels!3m6!1sHotels!2sErnakulam,+Kerala!3s0x3b080d08f976f3a9:0xe9cdb444f06ed454!4m2!1d76.2998842!2d9.9816358!3m7!1s0x3b080d4e1937ea55:0x69ec12f91b48b67e!5m2!4m1!1i2!8m2!3d9.9812658!4d76.2828804","https://www.google.co.in/maps/place/Holiday+Inn+Cochin,+an+IHG+Hotel/@9.9865677,76.3048252,14.17z/data=!4m18!1m9!2m8!1sHotels!3m6!1sHotels!2sErnakulam,+Kerala!3s0x3b080d08f976f3a9:0xe9cdb444f06ed454!4m2!1d76.2998842!2d9.9816358!3m7!1s0x3b080d21acb3edbb:0xb279fc9797cc341e!5m2!4m1!1i2!8m2!3d9.9902112!4d76.3158717"]
results={}
for index,url in enumerate(urls):
    x = WebDriver()
    results[index+1]=x.scrape(url)
result = json.dumps(results,indent=2)
print(result)