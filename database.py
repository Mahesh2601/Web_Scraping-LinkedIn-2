#import main
import json

import pymysql

# Database Connection

conn = pymysql.connect(host="127.0.0.1", user="root", passwd="", db="web_scraping-linkedin")
mycur = conn.cursor()


with open("categories_sub_categories.json") as c_s_c:
    data = json.load(c_s_c)
i = 0
j = 0

# for job_types_1 table

drop = "DROP TABLE job_types_1"
mycur.execute(drop)
create = "CREATE TABLE `job_types_1` ("\
    "`job_type1_id` int(3) PRIMARY KEY,"\
    "`categories` varchar(220) NOT NULL"\
    ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
mycur.execute(create)

# for job_types_2 table

drop = "DROP TABLE job_types_2"
mycur.execute(drop)
create = "CREATE TABLE `job_types_2` ("\
    "`job_type2_id` int(3) PRIMARY KEY,"\
    "`sub_categories` varchar(220) NOT NULL"\
    ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
mycur.execute(create)
for d in data:
    j += 1
    mycur.execute(
        f''' INSERT INTO job_types_1 VALUES ({i},'{d["category"]}')'''
    )
    for s in d["sub_categories"]:
        i += 1
        mycur.execute(
          f''' INSERT INTO job_types_2 VALUES ({i},'{s}')'''
        )

# for states table

drop = "DROP TABLE states"
mycur.execute(drop)
create = "CREATE TABLE `states` ("\
    "`state_id` int(3) PRIMARY KEY,"\
    "`state` varchar(220) NOT NULL"\
    ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
mycur.execute(create)
with open("description_location_employees.json") as l:
    data2 = json.load(l)

i = 0
for d in data2:
    i += 1
    mycur.execute(
        f''' INSERT INTO states VALUES ({i},'{d["location"]}')'''
    )


# for comapny_details table

with open("name_description_location_sub_categories.json") as c_d:
    data4 = json.load(c_d)
drop = "DROP TABLE company_details"
create = "CREATE TABLE `company_details` ("\
                "`sno` int(3) PRIMARY KEY,"\
                "`company_name` varchar(220) DEFAULT NULL,"\
                "`description` varchar(2200) DEFAULT NULL,"\
                "`state` varchar(220) DEFAULT NULL,"\
                "`sub_categories` varchar(220) DEFAULT NULL"\
         ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
mycur.execute(drop)
mycur.execute(create)
i = 0
for d in data4:
    i += 1
    mycur.execute(
        f'INSERT INTO company_details VALUES("{i}","{d["company_name"]}","{d["description"]}","{d["state"]}","{d["sub_categories"]}");'
    )


with open("position_company_location.json") as j:
    data3 = json.load(j)

# for jobs table

i = 0
drop = "DROP TABLE jobs"
mycur.execute(drop)
query = "CREATE TABLE jobs (" \
             "job_id int(3) PRIMARY KEY," \
             "company_name varchar(220) NOT NULL," \
             "position varchar(220) NOT NULL," \
             "location varchar(220) DEFAULT NULL" \
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
mycur.execute(query)

for d in data3:
    i += 1
    mycur.execute(
        f'INSERT INTO jobs VALUES("{i}","{d["company"]}","{d["position"]}","{d["location"]}");'
    )



conn.commit()
conn.close()

