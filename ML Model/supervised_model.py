from sklearn import datasets, linear_model
import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt
import random
import csv

# hardcode if normalize
normalize = 0
# declare filenames
csv_file_abs = 'candidates_final_financing_vectors.csv'
csv_file_normalized = 'candidates_final_financing_vectors_normalized.csv'
csv_file = 'temp'
# hyperparameters
num_bins = 40

# open csv to write normalized vectors
with open(csv_file_normalized, 'w', newline='') as csv_file:
    # declare file reader / writer
    normalized_writer = csv.writer(csv_file)
    with open(csv_file_abs) as csv_file1:
        csv_reader1 = csv.reader(csv_file1, delimiter=',')
        for row in csv_reader1:
            sum = 0
            idx = 0
            # get sum of all elements in row
            for cells in row:
                sum += float(cells)
            # reset elements ratio of sum
            for cells in row:
                if idx == 13:
                    break
                row[idx] = float(row[idx]) / sum
                idx += 1
            # output to normalized csv
            normalized_writer.writerow(row)

# Load the financing vectors dataset, original or normalized
if normalize:
    csv_file = csv_file_normalized
else:
    csv_file = csv_file_abs

# load vector dataset
pac_dataframe = genfromtxt('candidates_final_linreg_normalized.csv', delimiter=',')

# declare training set vector inputs
pac_training_inputs = np.delete(pac_dataframe, 13, 1)

# randomize PAC contributions in sector-wise fashion
idx = 0
while idx < 13:
    np.random.shuffle(pac_dataframe[:,idx])
    idx += 1

# declare randomized set vector inputs
pac_testing_inputs = np.delete(pac_dataframe, 13, 1)

# declare training set outputs
pac_training_outputs = pac_dataframe[:,13]

# create linear regression object
supervised_regression_model = linear_model.LinearRegression()

# Train the model using the training sets
supervised_regression_model.fit(pac_training_inputs, pac_training_outputs)

# Make predictions using the testing set
pac_predicted_outputs = supervised_regression_model.predict(pac_testing_inputs)

# declare plots with training outputs, predicted outpus
fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)
axs[0].hist(pac_training_outputs, bins=num_bins)
axs[1].hist(pac_predicted_outputs, bins=num_bins)

# show plot
plt.show()
