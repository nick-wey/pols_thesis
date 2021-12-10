import csv

# hardcode first election year with PAC fundraising data
year = '2018'
# while loop for each election year with data
while int(year) < 2020:
    # initialize flag and index variables
    found = 0
    line = 1
    # open csv's for dw-nominate matches, and not matches
    with open('senators_notfound.csv', 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        with open(year + '_hist_finaldata.csv', 'w', newline='') as csv_file0:
            csv_writer0 = csv.writer(csv_file0)
            csv_writer0.writerow(['Score','Funding','Senator'])
            # open csv's for dw-nominate and PAC fundraising data
            with open('DWNominate.csv',errors='ignore') as csv_file1:
                with open(year + '_senatePACrankings.csv') as csv_file2:
                    csv_reader = csv.reader(csv_file1, delimiter=',')
                    csv_reader2 = csv.reader(csv_file2, delimiter=',')
                    # loop through senator entries, parse for name
                    for row2 in csv_reader2:
                        last_name1 = row2[0].split('Jr')[0].strip().split(' ')[-1]
                        line = 0
                        csv_file1.seek(0)
                        found = 0
                        # loop through dw-nominate entreis, parse for name
                        for row1 in csv_file1:
                            print(line)
                            line += 1
                            if found == 1:
                                continue
                            last_name2 = row1.split(',')[1][1:]
                            # if name matches, get score, parse out suffix
                            if last_name1.lower() == last_name2.lower():
                                score = row1.split(',')[3].strip()
                                if score.__contains__('Jr.') or  score.__contains__('III'):
                                    score = row1.split(',')[4]
                                # write to output file, set found flag
                                csv_writer0.writerow([score, row2[1], row2[0]])
                                found = 1
                        # if not found, write to error file
                        if found == 0:
                            csv_writer.writerow([year, row2[0]])
        # increment year for while loop
        year = str(int(year) + 2)
