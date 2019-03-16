import sys
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import urllib
import json
import mysql.connector
import pymysql
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from config import get_conn

def get_data_frame():
    return pd.DataFrame(columns=('source', 'source_record_id', 'posted', 'link', 'title', 'description', 'location', 'other'))

def select_path(base, path):
    if (path.find("+") != -1):
        return select_path(base, path[0:path.find(" + ")].strip()) + select_path(base, path[path.find("+")+1:].strip())
    if (path[0] == "'" and path[-1] == "'"):
        return path[1:-1]
    result = ""
    regex = ""
    while True:
        if (path[0:3] == "../"):
            base = base.parent
            path = path[3:]
        elif (path[0:5] == "next("):
            tag = path[path.find("(") + 1 : path.find(")")]
            if (tag == ""):
                base = base.next_sibling
            else:
                base = base.find_next_sibling(tag)
            path = path[path.find(")") + 1 : ].strip("/")
        elif (path[0:5] == "prev("):
            tag = path[path.find("(") + 1 : path.find(")")]
            if (tag == ""):
                base = base.previous_sibling
            else:
                base = base.find_previous_sibling(tag)
            path = path[path.find(")") + 1 : ].strip("/")
        else:
            break
    if (path.find("/~") != -1):
        regex = path[path.find("/~") + 2:]
        path = path[0:path.find("/~")]
    if (path.find("~") == 0):
        regex = path[1:]
        path = ""
    if (path == "" or path == "."):
        result = base.text.strip()
    elif (path.find("/@") != -1):
        attr = path[path.find("/@") + 2:]
        path = path[0:path.find("/@")]
        result = base.select_one(path)[attr]
    else:
        result = base.select_one(path).text.strip()
    if (regex != ""):
        result = re.search(regex, result).group(1).strip()
    return re.sub(r'[^\x20-\x7F]+', ' ', result)
    #return result.encode("ascii", errors="ignore").decode()

def save_data_frame(data):
    sys.stdout.write("Saving " + str(len(data)) + " records: ")
    sys.stdout.flush()
    myconn = get_conn()
    mycursor = myconn.cursor(pymysql.cursors.DictCursor)
    for index, record in data.iterrows():
        sql = "select count(*) as num from job_posting inner join source on job_posting.source_id = source.id where source.source = %s and job_posting.source_record_id = %s"
        mycursor.execute(sql, (record["source"], record["source_record_id"]))
        myresult = mycursor.fetchone()
        if (myresult["num"] == 0):
            sql = "insert into job_posting ("
            for col in data.columns:
                if (col == "source"):
                    sql += "source_id" + ", "
                else:
                    sql += col + ", "
            values = ()
            sql = sql[0:len(sql) - 2] + ") values ( "
            for col in data.columns:
                if (col == "source"):
                    sql += "(select id from source where source = %s) , "
                else:
                    sql += "%s , "
            sql = sql[0:len(sql) - 2] + ")"
            mycursor.execute(sql, record.tolist())
            sys.stdout.write('+')
        else:
            sys.stdout.write('.')
        sys.stdout.flush()
    myconn.commit()
    mycursor.close()
    myconn.close()
    sys.stdout.write("\r\n")

def get_job_posting_urls():
    myconn = get_conn()
    mycursor = myconn.cursor(pymysql.cursors.DictCursor)
    mycursor.execute("select source.source, job_posting_url.* from job_posting_url inner join source on job_posting_url.source_id = source.id where url like '%kslaw.com/pages/%'")
    myresult = mycursor.fetchall()
    mycursor.close()
    myconn.close()
    return myresult

def scrape_viDesktop(url, source):
    base_url = url[0:url.find("ReDefault.aspx") - 1]
    data = get_data_frame()
    page_response = requests.get(url, timeout=5, verify=False)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    c7_divs = page_content.find_all("div", attrs={ "class": "c7" })
    for c7_div in c7_divs:
        try:
            row_div = c7_div.parent
            title = row_div.find("h4").text.strip()
            link_a = row_div.select_one("a[href*='ReJobView']")
            link = ""
            if (link_a != None): link = base_url + link_a["href"]
            description = row_div.find_next_sibling("div", attrs={ "class": "RichTextContent" }).text.strip()
            source_record_id = ""
            if (link != ""): source_record_id = re.search("JobID=(\\d*)", link).group(1).strip()
            data = data.append({ 'source': source, 'source_record_id': source_record_id, 'link': link, 'title': title, 'description': description, }, ignore_index=True)
        except Exception as e:
            print("An error occurred")
            print(e)
    return data

def scrape_jobvite(url, source):
    data = get_data_frame()
    page_response = requests.get(url, timeout=5, verify=False)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    tables = page_content.find_all("table", attrs={ "class": "jv-job-list" })
    for table in tables:
        tds = table.select("td.jv-job-list-name")
        for td in tds:
            try:
                tr = td.parent
                name_td = tr.find("td", attrs={ "class": "jv-job-list-name" })
                name_a = name_td.find("a")
                title = name_a.text.strip()
                link = "http://jobs.jobvite.com" + name_a["href"]
                location = tr.find("td", attrs={ "class": "jv-job-list-location" }).text.strip()
                source_record_id = re.search("/job/([A-Za-z0-9]*)", link).group(1).strip()
                data = data.append({ 'source': source, 'source_record_id': source_record_id, 'link': link, 'title': title, 'location': location }, ignore_index=True)
            except Exception as e:
                print("An error occurred")
                print(e)
    return data

def scrape_silkroad(url, source):
    base_url = url[0:url.find("index.cfm")]
    data = get_data_frame()
    page_response = requests.get(url, timeout=5, verify=False)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    trs = page_content.find_all("tr", attrs={ "class": "cssSearchResultsHighlight" })
    for tr in trs:
        try:
            tds = tr.find_all("td")
            title = tds[1].text.strip()
            link = base_url + tds[1].find("a")["href"]
            location = tds[2].text.strip()
            source_record_id = tds[0].text.strip()
            data = data.append({ 'source': source, 'source_record_id': source_record_id, 'link': link, 'title': title, 'location': location }, ignore_index=True)
        except Exception as e:
            print("An error occurred")
            print(e)
    return data

def scrape_taleo(url, source):
    pass

def scrape_json(params):
    data = get_data_frame()
    page_response = requests.get(params["url"], timeout=5)
    content = json.loads(page_response.content)
    for posting in content[params["each_posting_path"]]:
        try:
            title = ""
            description = ""
            source_record_id = ""
            posted = ""
            link = ""
            location = ""
            if (params["title_path"] != None and params["title_path"] != ""):
                title = posting[params["title_path"]]
            if (params["description_path"] != None and params["description_path"] != ""):
                description = posting[params["description_path"]]
            if (params["source_record_id_path"] != None and params["source_record_id_path"] != ""):
                source_record_id = posting[params["source_record_id_path"]]
            if (params["posted_path"] != None and params["posted_path"] != ""):
                posted = posting[params["posted_path"]]
            if (params["link_path"] != None and params["link_path"] != ""):
                link = posting[params["link_path"]]
            if (params["location_path"] != None and params["location_path"] != ""):
                location = posting[params["location_path"]]
            data = data.append({ 'source': params["source"], 'source_record_id': source_record_id, 'link': link, 'title': title, 'location': location, 'description': description, 'posted': posted }, ignore_index=True)
        except Exception as e:
            print("An error occurred")
            print(e)
    return data;

def scrape_custom(params):
    base_url = params["url"][0:params["url"].rfind("/") + 1]
    data = get_data_frame()
    page_response = requests.get(params["url"], timeout=5, verify=False)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    postings = page_content.select(params["each_posting_path"])
    for posting in postings:
        try:
            title = ""
            description = ""
            source_record_id = ""
            posted = ""
            link = ""
            location = ""
            if (params["title_path"] != None and params["title_path"] != ""):
                title = select_path(posting, params["title_path"])
            if (params["description_path"] != None and params["description_path"] != ""):
                description = select_path(posting, params["description_path"])
            if (params["source_record_id_path"] != None and params["source_record_id_path"] != ""):
                source_record_id = select_path(posting, params["source_record_id_path"])
            if (params["posted_path"] != None and params["posted_path"] != ""):
                posted = select_path(posting, params["posted_path"])
            if (params["link_path"] != None and params["link_path"] != ""):
                link = select_path(posting, params["link_path"])
            if (params["location_path"] != None and params["location_path"] != ""):
                location = select_path(posting, params["location_path"])
            data = data.append({ 'source': params["source"], 'source_record_id': source_record_id, 'link': link, 'title': title, 'location': location, 'description': description, 'posted': posted }, ignore_index=True)
        except Exception as e:
            print("An error occurred")
            print(e)
    return data

data = get_data_frame()
for url in get_job_posting_urls():
    print("Retrieving " + url["url"])
    prev_count = len(data)
    if (url["method"].lower() == "videsktop"):
        data = data.append(scrape_viDesktop(url["url"], url["source"]), ignore_index=True)
    if (url["method"].lower() == "jobvite"):
        data = data.append(scrape_jobvite(url["url"], url["source"]), ignore_index=True)
    if (url["method"].lower() == "silkroad"):
        data = data.append(scrape_silkroad(url["url"], url["source"]), ignore_index=True)
    if (url["method"].lower() == "taleo"):
        data = data.append(scrape_taleo(url["url"], url["source"]), ignore_index=True)
    if (url["method"].lower() == "custom"):
        data = data.append(scrape_custom(url), ignore_index=True)
    if (url["method"].lower() == "json"):
        data = data.append(scrape_json(url), ignore_index=True)
    print("New records: " + str(len(data)- prev_count))
    #print("Total records (cumulative): " + str(len(data)))
data = data.fillna("")
save_data_frame(data)
print(data.to_string())
print("Done.")

