# import packages
from selenium import webdriver
import csv
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

# hardcode year
year = '2008'
# open text file with pacs
pac_file = open(year + '_pacs.txt')
list_error_pacs = []

# for each pac in the text file
for pac in pac_file.readlines():
    # get pac name
    pac_name = pac.rstrip()
    # initilize Chrome webdriver
    chrome_driver = webdriver.Chrome()
    # open the opensecrets site with top pacs list for given year
    chrome_driver.get("https://www.opensecrets.org/pacs/toppacs.php?Type=C&pac=A&cycle=" + year)
    # print checkpoint
    print("Page Checkpoint")
    # get link to pac profile from pac name and click
    pac_link = chrome_driver.find_element_by_link_text(pac_name)
    pac_link.click()
    print("PAC URL Checkpoint")
    # get secondary link
    pac_link_2 = chrome_driver.find_elements_by_link_text(pac_name)
    print("PAC URL Checkpoint 2")
    # add to bad list if error in driver
    if not class_select:
        list_error_pacs.append(pac_name)
        continue
    pac_link_2[0].click()
    # get list recipients link
    recipients_link = chrome_driver.find_element_by_link_text("list recipients")
    recipients_link.click()
    print("Recipients URL Checkpoint")
    # specify the url
    url = chrome_driver.current_url
    quote_page = url[:-4] + year
    # build website request based off current url
    reqest = Request(quote_page, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(reqest)
    # parse the html with beautiful soup
    list_recipients_html = BeautifulSoup(page, 'html.parser')
    table = list_recipients_html.find('table', id="tab2")
    if table is None:
        list_error_pacs.append(pac_name)
        continue
    print("Table Found Checkpoint")
    table_rows = table.findAll('tr')
    i = 0
    # copy relevant elements from table into pacs contributions
    with open(year + '_pacs_contributions.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([pac_name,'','','','','','','',''])
        writer.writerow(['Last','First','Party','State','Contribution','Incumbency','Seniority','Close','Committee'])
        for row in table_rows:
                cells = row.findChildren('td')
                input_row = []
                for cell in cells:
                    line = cell.string
                    if (i == 0):
                        # parse out last name, first name, party, state
                        line_list = line.split('(')
                        line_list[0] = line_list[0][:-1]
                        party_state = line_list[1].split('-')
                        party_state[1] = party_state[1][:-1]
                        last_first_name = line_list[0].split(', ')
                        input_row = [last_first_name[0],last_first_name[1],party_state[0],party_state[1]]
                        i += 1
                    else:
                        # append contribtution to end of total
                        i -= 1
                        input_row.append(cell.string)
                        # append temp initializations for other candidate characteristics
                        input_row.append('')
                        input_row.append('')
                        input_row.append('')
                        input_row.append('')
                        writer.writerow(input_row)
# print pacs that throw error in this process for manual checks
print(list_error_pacs)
