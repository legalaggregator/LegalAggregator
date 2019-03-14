import sys
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import urllib
import json
import mysql.connector
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from config import get_conn

def get_data_frame():
    return pd.DataFrame(columns=('source', 'source_record_id', 'posted', 'link', 'title', 'description', 'location', 'other'))

def save_data_frame(data):
    sys.stdout.write("Saving " + str(len(data)) + " records: ")
    sys.stdout.flush()
    myconn = get_conn()
    mycursor = myconn.cursor()
    for index, record in data.iterrows():
        sql = "select count(*) from job_posting inner join source on job_posting.source_id = source.id where source.source = %s and job_posting.source_record_id = %s"
        mycursor.execute(sql, (record["source"], record["source_record_id"]))
        myresult = mycursor.fetchone()
        if (myresult[0] == 0):
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
    mycursor = myconn.cursor()
    mycursor.execute("select source.source, job_posting_url.url, job_posting_url.method from job_posting_url inner join source on job_posting_url.source_id = source.id")
    myresult = mycursor.fetchall()
    mycursor.close()
    myconn.close()
    return myresult

def scrape_lease_labau():
    data = get_data_frame()
    url = "http://www.leaselabau.com/jobs/JobSeeker/search.cfm?page=position-search"
    page_response = requests.get(url, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    title_tds = page_content.find_all("td", attrs={ 'class': 'job-post-title' })
    for title_td in title_tds:
        try:
            link_a = title_td.find("dt").find('a')
            other_td = title_td.find_next_sibling('td', attrs={ 'class': 'job-post-date' })
            title = title_td.find("dt").text.strip()
            description = title_td.find("dd").text.strip()
            other = other_td.text.strip().strip()
            link = "http://www.leaselabau.com/jobs/JobSeeker/" + link_a['href']
            source_record_id = urllib.parse.unquote(re.search("JobID=(.*)", link).group(1))
            data = data.append({ 'source': 'leaselabau.com', 'source_record_id': source_record_id, 'link': link, 'title': title,  'description': description, 'other': other }, ignore_index=True)
        except:
            pass
    return data

def scrape_ala():
    data = get_data_frame()
    url = "https://my.alanet.org/careers/jobs.asp?results=100"
    page_response = requests.get(url, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    title_tds = page_content.find_all("td", attrs={ 'class': 'jobtitle' })
    for title_td in title_tds:
        try:
            link_a = title_td.find('a')
            title_tr = title_td.parent
            location_tr = title_tr.find_next_sibling("tr")
            description_tr = location_tr.find_next_sibling("tr")
            other_tr = description_tr.find_next("span", attrs={ 'class': 'posnum' }).find_parent('tr')
            title = title_td.text.strip()
            location = location_tr.text.strip()
            description = description_tr.text.strip()
            other = other_tr.text.strip()
            link = "https://my.alanet.org/careers/" + link_a['href']
            source_record_id = urllib.parse.unquote(re.search("Ad #(A[0-9]*)\\D", other).group(1))
            data = data.append({ 'source': 'alanet.org', 'source_record_id': source_record_id, 'link': link, 'title': title,  'description': description, 'location': location, 'other': other }, ignore_index=True)
        except:
            pass
    return data

def scrape_mla():
    data = get_data_frame()
    url = "https://www.mlaglobal.com/enterprise/jobs/jobfeeddata?data=%7B%22keyword%22%3A%22%22%2C%22location%22%3A%22US%22%2C%22searchOnCountryLevel%22%3Atrue%2C%22paramArray%22%3A%5B%5D%2C%22count%22%3A100%2C%22page%22%3A%221%22%2C%22keyValueParameters%22%3A%7B%22%22%3Anull%7D%2C%22sortBy%22%3A%22Distance%22%2C%22pageId%22%3A%22%7B01E3CDA9-F753-4480-9B6E-79A0AE3CD0B0%7D%22%2C%22countryFilter%22%3Afalse%7D"
    page_response = requests.get(url, timeout=5)
    content = json.loads(page_response.content)
    for result in content["Results"]:
        data = data.append({ 'source': 'mlaglobal.com', 'source_record_id': result["Id"], 'link': result["JobUrl"], 'title': result["Title"],  'description': result["Teaser"], 'location': result["Location"], 'other': "" }, ignore_index=True)
    return data;

def scrape_kirkland_staff():
    data = get_data_frame()
    url = "https://staffjobsus.kirkland.com/jobs/search/?q=&location_city=&sort_by=cfml10%2Cdesc"
    page_response = requests.get(url, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    job_divs = page_content.find_all("div", attrs={ 'class': 'jobs-section__item' })
    for job_div in job_divs:
        title_h2 = job_div.find("h2")
        title_a = title_h2.find("a")
        title = title_a.text
        link = title_a["href"]
        source_record_id = re.search("jobs/(\d*)-", link).group(0)
        description = job_div.find("div", attrs={ "class": "jobs-section__item-hover-text" }).text
        location = ""
        posted = ""
        divs = job_div.find_all("div")
        for div in divs:
            if (div.text.__contains__("Location: ")):
                location = div.text.replace("Location: ", "")
            if (div.text.__contains__("Posted: ")):
                posted = div.text.replace("Posted: ", "")
        data = data.append({ 'source': 'kirkland.com', 'source_record_id': source_record_id, 'link': link, 'title': title,  'description': description, 'location': location, "posted": posted }, ignore_index=True)
    return data

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
            link = base_url + row_div.select_one("a[href*='ReJobView']")["href"]
            description = row_div.find_next_sibling("div", attrs={ "class": "RichTextContent" }).text.strip()
            source_record_id = re.search("JobID=(\\d*)", link).group(1).strip()
            data = data.append({ 'source': source, 'source_record_id': source_record_id, 'link': link, 'title': title, 'description': description, }, ignore_index=True)
        except:
            print("An error occurred")
    return data

def scrape_jobvite(url, source):
    data = get_data_frame()
    page_response = requests.get(url, timeout=5, verify=False)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    tables = page_content.find_all("table", attrs={ "class": "jv-job-list" })
    for table in tables:
        trs = table.find_all("tr")
        for tr in trs:
            try:
                name_td = tr.find("td", attrs={ "class": "jv-job-list-name" })
                name_a = name_td.find("a")
                title = name_a.text.strip()
                link = "http://jobs.jobvite.com" + name_a["href"]
                location = tr.find("td", attrs={ "class": "jv-job-list-location" }).text.strip()
                source_record_id = re.search("/job/([A-Za-z0-9]*)", link).group(1).strip()
                data = data.append({ 'source': source, 'source_record_id': source_record_id, 'link': link, 'title': title, 'location': location }, ignore_index=True)
            except:
                pass
    return data

def scrape_silkroad(url, source):
    pass

def scrape_silkroad(url, source):
    pass

data = get_data_frame()
for url in get_job_posting_urls():
    print("Retrieving " + url[1])
    if (url[2].lower() == "videsktop"):
        data = data.append(scrape_viDesktop(url[1], url[0]), ignore_index=True)
    if (url[2].lower() == "jobvite"):
        data = data.append(scrape_jobvite(url[1], url[0]), ignore_index=True)
    if (url[2].lower() == "silkroad"):
        data = data.append(scrape_silkroad(url[1], url[0]), ignore_index=True)
    if (url[2].lower() == "taleo"):
        data = data.append(scrape_taleo(url[1], url[0]), ignore_index=True)
    print("Total records (cumulative): " + str(len(data)))
#data = data.append(scrape_lease_labau(), ignore_index=True)
#data = data.append(scrape_ala(), ignore_index=True)
#data = data.append(scrape_mla(), ignore_index=True)
#data = data.append(scrape_kirkland_staff(), ignore_index=True)
data = data.fillna("")
save_data_frame(data)

# For completeness
# WilmerHale:
# - https://wilmerhale-openhire.silkroad.com/epostings/index.cfm?fuseaction=app.jobsearch
# - https://www.wilmerhale.com/en/careers/lawyers

# Mofo (various taleo):
# - https://careers.mofo.com/apply/



# kslaw.com:
# - kslaw.com has attorney positions posted on their website
# Ropes & Gray:
# - https://www.ropesgray.com/en/legalhiring/Career-Opportunities/Lateral-Associates/All-Positions
# - https://chm.tbe.taleo.net/chm02/ats/careers/v2/jobSearch?org=ROPESGRAY

#print(data)

print("Done.")

