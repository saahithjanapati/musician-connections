"""
this script extracts list of artist names from the following website:
https://chartmasters.org/most-streamed-artists-ever-on-spotify/

You still need to manually navigate to the page and make sure all 1000 artists are visible
TODO: Is it worth trying to do all of this automatically??? 
Almost all English artists who I'm aware of are in the top 1000.

Also note that the list is not entirely accurate.

Also, selenium is not included in the requirements.txt file cuz this code won't be running as part of the app.
So, if you wanna run this script, run pip install selenium first
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
input("Enter once you have naviagted to the list page and ALL artists are visible")
job_list = driver.find_elements_by_class_name("column-artist-name")
print(len(job_list))
artist_names = []
print(job_list[0].text)
for job in job_list[1:]:
    artist_names.append(job.text)


with open('artist_names.txt', 'w') as f:
    for item in artist_names:
        f.write("%s\n" % item)