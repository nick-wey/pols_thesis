import csv

# congress
congress = '115'
# dictionary mapping committees to indexes
committee = {'Agriculture, Nutrition, and Forestry':1, 'Commerce, Science, and Transportation':2,
    'Banking, Housing, and Urban Affairs':3, 'Armed Services':4, 'Judiciary':6, 'Environment and Public Works':5,
    'Health, Education, Labor, and Pensions':8, 'Energy and Natural Resources':7, 'Labor and Human Resources':8,
    'Homeland Security and Governmental Affairs':9, 'Governmental Affairs':9}
# list of state words for parsing purposes
states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida',
'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts',
'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico',
'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'Carolina',
'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming','Island','York']
# flags and temp variables
found = 0
committee_name = 'temp'
num_found = 0

# opening input and outpuf files
with open(congress + '_membership_processed.csv', 'w', newline='') as csv_file_1:
    output_writer = csv.writer(csv_file_1)
    with open(congress + '.csv') as csv_file_2:
        text = csv.reader(csv_file_2, delimiter=',')
        # parsing row
        for row in text:
            # found committee region
            if found == 1 and len(row) > 0:
                if ', of' in row[0]:
                    row1 = row[0].split(', of')
                    # row has multiple names
                    if (len(row1) == 2):
                        split = row1[0].split('.', 1)
                        if split[0].lstrip() in states:
                            output_writer.writerow([committee_name, split[1].lstrip().split(", Jr.")[0]])
                        else:
                            output_writer.writerow([committee_name, row1[0].lstrip().split(", Jr.")[0]])
                    else:
                        # row has one name
                        if(len(row1)==1):
                            continue
                        else:
                            output_writer.writerow([committee_name, row1[0].split(", Jr.")[0]])
                            breaks = row1[1].split(' ')
                            if breaks[1] == 'West' or breaks[1] == 'New' or breaks[1] =='Rhode' or breaks[1] =='South':
                                if breaks[2] == '':
                                    idx = 0
                                    str0 = ''
                                    for element in breaks:
                                        if idx > 1:
                                            if element != '':
                                                str0 += element + ' '
                                        idx += 1
                                    output_writer.writerow([committee_name, str0.strip().split(", Jr.")[0]])
                                    continue
                            second = row1[1].split('.', 1)
                            if len(second) == 1:
                                output_writer.writerow([committee_name, second[0].lstrip().split(", Jr.")[0]])
                            if second[0].strip() not in states:
                                str4 = ''
                                for ele in second:
                                    str4 += ele.strip() + ' '
                                output_writer.writerow([committee_name, str4.strip().split(", Jr.")[0]])
                            else:
                                output_writer.writerow([committee_name, second[1].lstrip().split(", Jr.")[0]])
            if len(row) == 1:
                text = row[0].lstrip().rstrip()
                if text in committee:
                    found = 1
                    num_found += 1
                    committee_name = committee.get(text)
                if text == "SUBCOMMITTEES":
                    found = 0
print('committees found: ' + str(num_found))
