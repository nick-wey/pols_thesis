import csv

first = 1

sector_dict = {}

drop = ['Every Republican is Crucial PAC','Majority Cmte PAC']

with open('weighted_pac_sector_info.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    for pac in csv_reader:
        if first == 1:
            first = 0
            continue
        pac_name = pac[0]
        if pac_name in drop:
            continue
        sector = pac[1]
        incr_vect = []
        for i in range(11):
            i += 2
            incr_vect.append(float(pac[i]))
        print(incr_vect)
        if sector in sector_dict:
            num_pacs = sector_dict[sector][0]
            cur_incr_vect = sector_dict[sector][1]
            for i in range(11):
                cur_incr_vect[i] += incr_vect[i]
            num_pacs += 1
            sector_dict[sector] = [num_pacs, cur_incr_vect]
        else:
            sector_dict[sector] = [1, incr_vect]

print(sector_dict)
with open('sector_final_data.csv','w',newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['pac',1998,2000,2002,2004,2006,2008,2010,2012,2014,2016,2018])
    for sector in sector_dict:
        row = [sector]
        value = sector_dict[sector]
        num_pacs = value[0]
        vector = value[1]
        for agg_inc_r in vector:
            row.append(agg_inc_r / num_pacs)
        row.append(num_pacs)
        print(row)
        writer.writerow(row)
