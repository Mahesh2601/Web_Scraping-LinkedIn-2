from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.errorhandler import NoSuchElementException
import json

COUNTRY = "India"
EMAIL = "maheswar2601@gmail.com"
PASSWORD = "Maheswar@2634"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


# Getting All Jobs from CareerGuide

driver.get("https://www.careerguide.com/career-options")
categories = dict()
sub_categories = []
for i in range(1, 14):
    for j in range(1, 4):
        if (i == 8 and j == 2) or (i == 6 and j == 1):
            continue
        sub_cats = []
        cat = driver.find_element(By.XPATH,
                                  f'//*[@id="aspnetForm"]/div[6]/div[3]/div/div[2]/div/div[{i}]/div[{j}]/h2/a')
        sub_cat = driver.find_elements(By.XPATH,
                                       f'//*[@id="aspnetForm"]/div[6]/div[3]/div/div[2]/div/div[{i}]/div[{j}]/ul/li/a')
        for k in sub_cat:
            sub_categories.append(k.text)
            sub_cats.append(k.text)
        categories[cat.text] = sub_cats

print(sub_categories)
categories_values = [c for c in categories.keys()]
print(categories_values)

print(categories)

# logging in LinkedIn


driver.get("https://www.linkedin.com/checkpoint/lg/sign-in-another-account")

username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")

time.sleep(1)
username.send_keys(EMAIL)
password.send_keys(PASSWORD)
password.send_keys(Keys.ENTER)

print(len(sub_categories))

# scraping position, company_name and location (remote,on-site) for the jobs

pos_com_loc = []
sub_categories_for_companies = dict()
for i in categories["Information Technology / Software"]:
    try:
        driver.get(f"https://www.linkedin.com/jobs/search/?keywords={i}&location={COUNTRY}&refresh=true")
        time.sleep(2)

        position = driver.find_elements(By.XPATH,
                                        '/html/body/div[4]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li'
                                        '/div/div[1]/div[1]/div[2]/div[1]/a')
        company = driver.find_elements(By.XPATH,
                                       '/html/body/div[4]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li'
                                       '/div/div[1]/div[1]/div[2]/div[2]/span/a')
        location = driver.find_elements(By.XPATH,
                                        '/html/body/div[4]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li'
                                        '/div/div[1]/div[1]/div[2]/div[3]/ul/li')


        positions = [p.text for p in position]
        companies = [c.text for c in company]
        locations = [l.text for l in location]

        pos_com_loc += list(zip(positions, companies, locations))
        pos_com_loc = list(set(pos_com_loc))
        sub_categories_for_companies[i] = companies

    except:
        continue

print(pos_com_loc)
jobs = [(c, p, l) for p, c, l in pos_com_loc]
print(jobs)

# scraping company_description, company_location and No.of Employees for the companies

companies = list(set([com[1] for com in pos_com_loc]))

des_loc_emp = []
com_des_state_subcategory = []

for com in companies:
    try:

        # searching the company by url
        driver.get(f"https://www.linkedin.com/search/results/COMPANIES/?keywords={com}")

        # clicking on the first link from the search
        try:
            driver.find_element(By.XPATH,
                                '//*[@id="main"]/div/div/div[1]/ul/li[1]/div/div/div[2]/'
                                'div[1]/div[1]/div/span/span/a').click()
        except:
            driver.find_element(By.XPATH,
                                '//*[@id="main"]/div/div/div[2]/ul/li[1]/div/div/div[2]'
                                '/div[1]/div[1]/div/span/span/a').click()
        finally:
            time.sleep(3)
            # going to about page of company by url
            driver.get(f"{driver.current_url}about/")

            # retrieving the description, location and no. of Employees of the company
            description = driver.find_element(By.XPATH, '//*[@id="main"]/div[2]/div/div/div[1]/section/p').text
            try:
                location = driver.find_element(By.XPATH,
                                               '//*[@id="main"]/div[2]/div/div/div[1]/section/dl/'
                                               'dt[contains(.,"Headquarters")]/following-sibling::dd').text
            except NoSuchElementException:
                location = "NULL"
            employee = driver.find_element(By.XPATH,
                                           '//*[@id="main"]/div[2]/div/div/div[1]/section/dl/'
                                           'dd[contains(.,"employees")]').text

            des_loc_emp.append((description, location, employee))
            com_des_state_subcategory.append((com, description, location, [s for s in sub_categories_for_companies if
                                                                           com in sub_categories_for_companies[s]]))

    except NoSuchElementException:
        continue

print(des_loc_emp)
print(com_des_state_subcategory)
states = list(set([loc[1] for loc in des_loc_emp]))
print(states)

# putting all the information in csv files

# 1.Jobs

with open("categories_sub_categories.json", "w") as f:
    f.write('[]')

for c in categories_values:
    data = {
        "category": c,
        "sub_categories": categories[c]
    }
    with open("categories_sub_categories.json", "r+") as f:
        c_s_c = json.load(f)
        c_s_c.append(data)
        f.seek(0)
        json.dump(c_s_c, f, indent=4)

# 2. Positon, Company, Location(remote/on-site)

with open("position_company_location.json", "w") as p_c_l:
    p_c_l.write('[]')

for p, c, l in pos_com_loc:
    data = {
        "position": p,
        "company": c,
        "location": l
    }
    with open("position_company_location.json", "r+") as p_c_l:
        f_d = json.load(p_c_l)
        f_d.append(data)
        p_c_l.seek(0)
        json.dump(f_d, p_c_l, indent=4)

# 3. Company_description, Company_location, No. of Employees

with open("description_location_employees.json", "w") as d_l_e:
    d_l_e.write('[]')

for d, l, e in des_loc_emp:
    data = {
        "description": d,
        "location": l,
        "no. of employees": e
    }
    with open("description_location_employees.json", "r+") as d_l_e:
        f_d = json.load(d_l_e)
        f_d.append(data)
        d_l_e.seek(0)
        json.dump(f_d, d_l_e, indent=4)

with open("name_description_location_sub_categories.json", "w") as n_d_l_s:
    n_d_l_s.write('[]')

for n, d, l, s in com_des_state_subcategory:
    data = {
        "company_name": n,
        "description": d,
        "state": l,
        "sub_categories": s
    }
    with open("name_description_location_sub_categories.json", "r+") as n_d_l_s:
        d = json.load(n_d_l_s)
        d.append(data)
        n_d_l_s.seek(0)
        json.dump(d, n_d_l_s, indent=4)

print("Done!")
