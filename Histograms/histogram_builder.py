import csv

# hardcode first election year with PAC fundraising data
year = '2000'
# while loop for each election year with data
while int(year) < 2020:
    # initialize flag, index, aggregator variables
    first = 1
    num_candidates_counted = 1
    v_radical_d_dol = 0
    v_radical_d_num = 0
    s_radical_d_dol = 0
    s_radical_d_num = 0
    s_moderate_d_dol = 0
    s_moderate_d_num = 0
    v_moderate_d_dol = 0
    v_moderate_d_num = 0
    v_moderate_r_dol = 0
    v_moderate_r_num = 0
    s_moderate_r_dol = 0
    s_moderate_r_num = 0
    s_radical_r_dol = 0
    s_radical_r_num = 0
    v_radical_r_dol = 0
    v_radical_r_num = 0
    # open final output file
    with open(year + '_hist_outputs_25.csv', 'w', newline='') as csv_file_1:
        output_writer = csv.writer(csv_file_1)
        output_writer.writerow(['Category','Amount'])
        # open reading file
        with open(year + '_hist_processed_data.csv') as csv_file_2:
            processed_data_reader = csv.reader(csv_file_2, delimiter=',')
            for row in processed_data_reader:
                # exclude first row
                if first == 1:
                    first = 0
                    continue
                # if number of candidates counted above 40, break
                if num_candidates_counted > 40:
                    break
                # if score does not exist, move to next entry
                if row[0] == '':
                    continue
                # change datatype of dw-nominate score to float
                dw_score = float(row[0])
                # compare and break into dw-nominate bins
                if dw_score < -0.75:
                    # index into row to get total dollar amount, add to aggregator
                    v_radical_d_dol += int(row[1])
                    # increment number in bin aggregator
                    v_radical_d_num += 1
                # repeat same constriction for all bins
                if -0.75 <= dw_score < -0.5:
                    s_radical_d_dol += int(row[1])
                    s_radical_d_num += 1
                if -0.5 <= dw_score < -.25:
                    s_moderate_d_dol += int(row[1])
                    s_moderate_d_num += 1
                if -.25 <= dw_score < 0:
                    v_moderate_d_dol += int(row[1])
                    v_moderate_d_num += 1
                if 0 <= dw_score < .25:
                    v_moderate_r_dol += int(row[1])
                    v_moderate_r_num += 1
                if .25 <= dw_score < 0.5:
                    s_moderate_r_dol += int(row[1])
                    s_moderate_r_num += 1
                if .5 <= dw_score < 0.75:
                    s_radical_r_dol += int(row[1])
                    s_radical_r_num += 1
                if 0.75 <= dw_score:
                    v_radical_r_dol += int(row[1])
                    v_radical_r_num += 1
                num_candidates_counted +=1
            # after all rows aggregated, output dollar summations for each bin
            output_writer.writerow(['v_radical_d_dol',v_radical_d_dol])
            output_writer.writerow(['s_radical_d_dol',s_radical_d_dol])
            output_writer.writerow(['s_moderate_d_dol',s_moderate_d_dol])
            output_writer.writerow(['v_moderate_d_dol',v_moderate_d_dol])
            output_writer.writerow(['v_moderate_r_dol',v_moderate_r_dol])
            output_writer.writerow(['s_moderate_r_dol',s_moderate_r_dol])
            output_writer.writerow(['s_radical_r_dol',s_radical_r_dol])
            output_writer.writerow(['v_radical_r_dol',v_radical_r_dol])
            # output relative percentage of senators in each bin
            output_writer.writerow(['v_radical_d_num',v_radical_d_num/40])
            output_writer.writerow(['s_radical_d_num',s_radical_d_num/40])
            output_writer.writerow(['s_moderate_d_num',s_moderate_d_num/40])
            output_writer.writerow(['v_moderate_d_num',v_moderate_d_num/40])
            output_writer.writerow(['v_moderate_r_num',v_moderate_r_num/40])
            output_writer.writerow(['s_moderate_r_num',s_moderate_r_num/40])
            output_writer.writerow(['s_radical_r_num',s_radical_r_num/40])
            output_writer.writerow(['v_radical_r_num',v_radical_r_num/40])
            # increment year to get to next election cycle
            year = str(int(year) + 6)
