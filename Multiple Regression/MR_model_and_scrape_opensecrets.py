# import packages

import csv
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
import numpy as np

# flags for different parts of script
scrape_done = 1
incumbents_only = 1
first = 1

# useful years indexing array
years = [1998,2000,2002,2004,2006,2008,2010,2012,2014,2016,2018]

# mapping states to regions
regions = {'AL':'south', 'AK':'west', 'AZ':'west', 'AR':'south', 'CA':'west', 'CO':'west', 'CT':'northeast','DE':'south', 'FL':'south', 'GA':'south',
'HI':'west', 'IL':'midwest', 'ID':'west', 'ID':'midwest', 'IN':'midwest', 'IA':'midwest', 'KS':'midwest', 'KY':'south', 'LA':'south', 'ME':'northeast', 'MD':'south',
'MA':'northeast', 'MI':'midwest', 'MN':'midwest','MS':'south', 'MO':'midwest', 'MT':'west', 'NE':'midwest', 'NV':'west', 'NH':'northeast', 'NJ':'northeast',
'NM':'west', 'NY':'northeast', 'NC':'south', 'ND':'midwest', 'OH':'midwest', 'OK':'south', 'OR':'west', 'PA':'northeast', 'RI':'northeast', 'SC':'south',
'SD':'midwest','TN':'south', 'TX':'south', 'UT':'west', 'VT':'northeast', 'VA':'south', 'WA':'west', 'WV':'south', 'WI':'midwest', 'WY':'west'}

# mapping sectors to encoded committee nums
sector_to_committee = {'Health':8,'Labor':8,'Energy & Natural Resources':7,'Transportation':2,'Education':8,'Defense':4,'Ideological & Single Issue':9,
'Communications & Electronics':2,'Food & Beverage':1,'Finance & Insurance & Real Estate':3,'Construction':5,'Lawyers & Lobbyists':6}

# encoding states and regions to numbers before setting up dummy variables
region_encode = {'south':1,'west':2,'northeast':3,'midwest':4}
party_encode = {'D':1,'R':2,'I':3,'3':3}

# initialize pac dictionary
pac_dict = {}

# if the scrape is done and saved down, skip this
if scrape_done == 0:
    pac_cid_array = []
    # read in basic info of all PACs (i.e. url codes from data)
    with open('PAC_data.csv') as csv_file:
        pac_data_reader = csv.reader(csv_file)
        for pac_info in pac_data_reader:
            if first == 1:
                first = 0
                continue
            pac_cid_array.append([pac_info[0],pac_info[1],pac_info[2]])

    # scrape for PAC contributions information
    list_bad = []
    for pac in pac_cid_array:
        pac_name = pac[0]
        committee_id = pac[1]
        sector = pac[2]
        all_pac_years_array = []
        # loop through all years
        for year in years:
            total_contributions = 0
            # build relevant url
            url = 'https://www.opensecrets.org/pacs/pacgot.php?cycle=' + str(year) + '&cmte=' + committee_id
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            page = urlopen(req)
            soup = BeautifulSoup(page, 'html.parser')
            # checkpoint
            print('found link')
            table = soup.find('table', id="tab2")
            if table is None:
                list_bad.append([pac_name, year])
                continue
            # checkpoint
            print('found table')
            # access, parse, and store contribution information from table
            table_rows = table.findAll('tr')
            # array for storing this info
            pac_cand_array = []
            for candidate in table_rows:
                indiv_cand_info = []
                cells = candidate.findChildren('td')
                row = []
                i = 0
                for cell in cells:
                    line = cell.string
                    # line variable example: "Aderholt, Robert B (R-AL)"
                    if (i == 0):
                        name_else = line.split('(')
                        first_last = name_else[0][:-1].split(', ')
                        last = first_last[0]
                        first = first_last[1].strip()
                        party_state = name_else[1].split('-')
                        state = party_state[1][:-1]
                        party = party_state[0]
                        indiv_cand_info = [last,first,party_encode.get(party),region_encode.get(regions.get(state))]
                        i += 1
                    else:
                        i -= 1
                        # cell.string example possibilities: $10,000; $0; ($2,000)
                        raw_contribution = cell.string
                        if '(' in raw_contribution:
                            raw_contribution = raw_contribution[2:-1]
                        else:
                            raw_contribution = raw_contribution[1:]
                        int_contribution = int(raw_contribution.replace(',',''))
                        total_contributions += int_contribution
                        indiv_cand_info = [int_contribution] + indiv_cand_info
                        # break in case third row in cells which is non-data
                        break
                # add candidate info into array represnting cycle
                pac_cand_array.append(indiv_cand_info)
            # add cycle info into array representing the entire PAC
            all_pac_years_array.append([year, total_contributions, pac_cand_array[1:]])
        # add PAC info into dictionary storing data on all pacs
        pac_dict[pac_name] = [sector, all_pac_years_array]

    # read pac dictionary into .csv file
    with open('opensecrets_pac_data.csv', 'w', newline='') as csv_file_pac:
        writer = csv.writer(csv_file_pac)
        for key in pac_dict:
            pac_name = key
            val_array = pac_dict[key]
            sector = val_array[0]
            pac_years_cont = val_array[1]
            for year in pac_years_cont:
                yr = year[0]
                total_cont = year[1]
                cand_arr = year[2]
                for candidate in cand_arr:
                    row = [pac_name,sector,yr,total_cont] + candidate
                    writer.writerow(row)

# the case that the scraping has already been completed, we re-build global pac_dict
else:
    with open('opensecrets_pac_data.csv') as csv_data_scrape:
        data_scrape_reader = csv.reader(csv_data_scrape)
        # first ones
        cur_pac = 'American Medical Assn'
        cur_sector = 'Health'
        all_pac_yrs_arr = []
        cand_matrix = []
        year = 1998
        # get info from each line
        for observation in data_scrape_reader:
            pac_name = observation[0]
            pac_sector = observation[1]
            year_i = int(observation[2])
            agg_year_cont = int(observation[3])
            contribution_amt = int(observation[4])
            last_name = observation[5]
            first_name = observation[6]
            if observation[7] == '':
                observation[7] = 3
            party_enc = int(observation[7])
            state_enc = int(observation[8])
            # build cand matrix
            cand_info = [contribution_amt,last_name,first_name,party_enc,state_enc]
            # for enties in same year, keep aggregating
            if pac_name == cur_pac and year_i == year:
                cand_matrix.append(cand_info)
            # when we see new entry from different year, start new year
            if pac_name == cur_pac and year_i != year:
                pac_year_obs = [year,agg_year_cont,cand_matrix]
                all_pac_yrs_arr.append(pac_year_obs)
                cand_matrix = [cand_info]
                year = year_i
            # when we seee new entry from different pac, start new pac
            if pac_name != cur_pac:
                pac_year_obs = [year,agg_year_cont,cand_matrix]
                all_pac_yrs_arr.append(pac_year_obs)
                pac_entry = [cur_sector, all_pac_yrs_arr]
                pac_dict[cur_pac] = pac_entry
                cand_matrix = [cand_info]
                pac_year_obs = []
                all_pac_yrs_arr = []
                year = year_i
                cur_pac = pac_name
                cur_sector = pac_sector
        # one last time for last pac outside of loop
        pac_year_obs = [year_i,agg_year_cont,cand_matrix]
        all_pac_yrs_arr.append(pac_year_obs)
        pac_entry = [cur_sector, all_pac_yrs_arr]
        pac_dict[pac_name] = pac_entry

# visualize to make sure data looks good
for key in pac_dict:
    print(key)
    val = pac_dict[key]
    sector = val[0]
    for yrs in val[1]:
        print(yrs)

# build incumbents matrix for each year
incumbents = []
for year in years:
    yr_inc = []
    # get incumbency file from relative directory
    with open('SenateIncumbents\\' + str(year) + '_incumbency.csv') as csv_file_inc:
        csv_reader_inc = csv.reader(csv_file_inc)
        first = 1
        print(year)
        # parse files into usable data form, subset logic for different style files
        if year == 2018 or year == 2016:
            for row in csv_reader_inc:
                if first == 1:
                    first = 0
                    rank = 1
                else:
                    rank = row[0]
                last_name = row[1].split(' ')[-1].strip()
                # append senator info to year
                yr_inc.append([last_name,int(rank)])
        else:
            for row in csv_reader_inc:
                last_name = 'temp'
                if first == 1:
                    first = 0
                    rank = 1
                else:
                    rank = row[0]
                name = row[1].split('(')[0].strip()
                name = name.split('[')[0].strip()
                name = name.split(', Jr.')[0].strip()
                name = name.split(' ')
                if len(name) >= 3:
                    last_name = name[2]
                else:
                    last_name = name[1]
                # append senator info to year
                yr_inc.append([last_name,int(rank)])
    # append year info to global array
    incumbents.append([year, yr_inc])
# print output to see if makes sense
print(incumbents)

# build committee membership array of dictionaries for each year
years_committees_dict = []
for year in years:
    committees_dict = {}
    yr_com = []
    # get committee file from relateive directory
    with open('SenateCommittees\\' + str(year) + '_membership_processed.csv') as csv_file_com:
        csv_reader_com = csv.reader(csv_file_com)
        # parse and store info into dictionary for each committee
        for row in csv_reader_com:
            c_num = int(row[0])
            name = row[1].split(' ')
            last_name = name[1]
            if len(name) > 2:
                last_name = name[2]
            if c_num in committees_dict:
                committees_dict[c_num] = committees_dict.get(c_num) + [last_name]
            else:
                committees_dict[c_num] = [last_name]
    # append dictionaries to global array
    years_committees_dict.append([year,committees_dict])
# print output to see if makes sense
print(years_committees_dict)

# initialize dictionary for pacs
pac_dict_inc_r = {}

# non-persistent or duplicate pacs
drop = ['Every Republican is Crucial PAC','Majority Cmte PAC','SBC Communications',
'American Fedn of St/Cnty/Munic Employees','American Assn for Justice']

print(pac_dict)
extra = ''
if incumbents_only == 1:
    extra = '_inc_only'

# open final output file
with open('opensecrets_pac_final_data' + extra + '.csv', 'w', newline='') as csv_file2:
    writer = csv.writer(csv_file2)
    coefficients_all_pacs = {}
    # for each pac in the dictionary, set up coefficients_matrix to get incremental_r_squared calclation
    for pac_name in pac_dict:
        coefficients_matrix = []
        print(pac_name)
        value = pac_dict[pac_name]
        sector = value[0]
        committee_num = sector_to_committee.get(sector)
        conts = value[1]
        new_val_array = []
        new_val_array_inc_r = []
        # for each year we run the regression, need to build regression row
        for yr_cont in conts:
            year = yr_cont[0]
            total_contributions = yr_cont[1]
            year_dict = years_committees_dict[years.index(year)][1]
            contributions_matrix = yr_cont[2]
            # this gives election margin info
            with open('SenateCandidates\\' + str(year) + '_SenateCandidates_processed.csv') as csv_file_cand:
                csv_reader_cand = csv.reader(csv_file_cand)
                for candidate in csv_reader_cand:
                    # Model: [Contribution,Last,First,Party,State,Election Margin, Incumbency, Seniority]
                    # build per-candiate regression array
                    last_name = candidate[0]
                    first_name = candidate[1]
                    party = candidate[2]
                    state = candidate[3]
                    election_margin = float(candidate[7])
                    indiv_cand_info = [0,last_name,first_name,party_encode.get(party),region_encode.get(regions.get(state)),election_margin]
                    found = 0
                    # just add election margin for candidates already in array, or entire entry for non-contributed to major party candidates
                    for i in range(len(contributions_matrix)):
                        entry = contributions_matrix[i]
                        # fill in not found
                        if len(entry) == 6:
                            continue
                        if last_name == entry[1]:
                            contributions_matrix[i].append(election_margin)
                            found = 1
                            break
                    if found == 0:
                        contributions_matrix.append(indiv_cand_info)
                minus = 0
                # fill in incumbency and seniority information
                for i in range(len(contributions_matrix)):
                    i -= minus
                    c_info = contributions_matrix[i]
                    last_name = c_info[1]
                    if len(c_info) != 6:
                        contributions_matrix[i].append(100)
                    incumbents_array = incumbents[years.index(year)][1]
                    found = 0
                    for val in incumbents_array:
                        if last_name == val[0]:
                            contributions_matrix[i].append(1)
                            contributions_matrix[i].append(val[1])
                            found = 1
                            break
                    if found == 0:
                        # for subsetting data on incumbents only
                        if incumbents_only == 1:
                            del contributions_matrix[i]
                            minus += 1
                            continue
                        else:
                            contributions_matrix[i].append(0)
                            contributions_matrix[i].append(110)
                    # fill in committee info if relevant sector and it exists
                    if committee_num in year_dict:
                        names_list = year_dict[committee_num]
                        if last_name in names_list:
                            contributions_matrix[i].append(1)
                        else:
                            contributions_matrix[i].append(0)
            # perform multiple linear regression, calculate incremnetal rsquared
            lm_party = linear_model.LinearRegression()
            lm_no_party = linear_model.LinearRegression()
            # set up dummy variables for categorical data (i.e patry and geographic region)
            X = contributions_matrix
            new_X = []
            for row in X:
                print(row)
                new_row = []
                val_add = 0
                for i in range(len(row)):
                    # party categories
                    if i == 3:
                        if row[i] == 1:
                            new_row += [1,0,0]
                        if row[i] == 2:
                            new_row += [0,1,0]
                        if row[i] == 3:
                            new_row += [0,0,1]
                    # region categories
                    elif i == 4:
                        if row[i] == 1:
                            new_row += [1,0,0,0]
                        if row[i] == 2:
                            new_row += [0,1,0,0]
                        if row[i] == 3:
                            new_row += [0,0,1,0]
                        if row[i] == 4:
                            new_row += [0,0,0,1]
                    else:
                        new_row.append(row[i])
                    # print(new_row)
                print(new_row)
                new_X.append(new_row)
            X = new_X
            # initialize training dataset
            x_train_party = []
            x_train_no_party = []
            y_train = []
            # convert all values to floats
            # append relevant information onto regression vectors
            for row in X:
                x_p_vect = []
                x_np_vect = []
                for i in range(len(row)):
                    if i == 0:
                        y_i = float(row[i])
                        y_train.append(y_i)
                    if i > 2:
                        x_i = float(row[i])
                        x_p_vect.append(x_i)
                    if i > 5:
                        x_i = float(row[i])
                        x_np_vect.append(x_i)
                x_train_party.append(x_p_vect)
                x_train_no_party.append(x_np_vect)
            # run multiple linear regression with party
            lm_party.fit(x_train_party,y_train)
            # get r-squared with party
            score_party = lm_party.score(x_train_party,y_train)
            # get regression coefficients
            if get_coefficients:
                lm = lm_party
                params = np.append(lm.intercept_,lm.coef_)
                print(params)
                coefficients_matrix.append(params)
            # run multiple linear regression with party dropped
            lm_no_party.fit(x_train_no_party,y_train)
            # get r-squared without party
            score_no_party = lm_no_party.score(x_train_no_party,y_train)
            # calculate incremental r-squared
            incremental_r_squared = score_party - score_no_party
            # calcualte % of total r-squared
            rel_r_squared = incremental_r_squared / score_party
            # append this information to new array
            new_val_array.append([year, total_contributions, contributions_matrix])
            new_val_array_inc_r.append([year, total_contributions, incremental_r_squared, rel_r_squared])
        # store relevant information into dictionaries
        coefficients_all_pacs[pac_name] = (coefficients_matrix)
        pac_dict[pac_name] = [sector, new_val_array]
        pac_dict_inc_r[pac_name] = [sector, new_val_array_inc_r]

    # transcribe dictionaries into csv
    inc_r_dynamics = []
    contrinution_amt_dynamics = []
    rel_r_squared_dynamics = []
    # build rows representing incremental r-squared, % of total, and contribution amount
    for key in pac_dict_inc_r:
        row1 = [key]
        row2 = [key]
        row3 = [key]
        val = pac_dict_inc_r[key]
        inc_array = val[1]
        for year in inc_array:
            contribution_total = year[1]
            incremental_r_squared = year[2]
            rel_r_sq = year[3]
            row1.append(incremental_r_squared)
            row2.append(contribution_total)
            row3.append(rel_r_sq)
        inc_r_dynamics.append(row1)
        contrinution_amt_dynamics.append(row2)
        rel_r_squared_dynamics.append(row3)
    # write rows
    for row in inc_r_dynamics:
        writer.writerow(row)
    for row in contrinution_amt_dynamics:
        writer.writerow(row)
    for row in rel_r_squared_dynamics:
        writer.writerow(row)
