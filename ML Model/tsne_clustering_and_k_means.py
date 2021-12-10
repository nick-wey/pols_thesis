from sklearn import datasets
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from numpy import genfromtxt
import numpy as np
from sklearn.cluster import KMeans
import csv

regions = {'AL':'s', 'AK':'w', 'AZ':'w', 'AR':'s', 'CA':'w', 'CO':'w', 'CT':'n','DE':'s', 'FL':'s', 'GA':'s',
'HI':'w', 'IL':'c', 'ID':'w', 'ID':'c', 'IN':'c', 'IA':'c', 'KS':'c', 'KY':'s', 'LA':'s', 'ME':'n', 'MD':'s',
'MA':'n', 'MI':'c', 'MN':'c','MS':'s', 'MO':'c', 'MT':'w', 'n':'c', 'NV':'w', 'NH':'n', 'NJ':'n',
'NM':'w', 'NY':'n', 'NC':'s', 'ND':'c', 'OH':'c', 'OK':'s', 'OR':'w', 'PA':'n', 'RI':'n', 'SC':'s',
'SD':'c','TN':'s', 'TX':'s', 'UT':'w', 'VT':'n', 'VA':'s', 'WA':'w', 'WV':'s', 'WI':'c', 'WY':'w'}

# define hyperparameters
num_perplexity = 40
num_learning_rate = 100
cluster_optimization = 7

# define input text file
csv_file = 'candidates_final_test.csv'

# load vector dataset
member_vectors_dataframe = genfromtxt(csv_file, delimiter=',')
# print(member_vectors_dataframe)
# remove dw-nominate for unsupervised data
rm_dw_member_vectors_dataframe = np.delete(member_vectors_dataframe, 13, 1)
# rm_dw_member_vectors_dataframe = member_vectors_dataframe[:,:-7]
# print(rm_dw_member_vectors_dataframe)
# print(rm_dw_member_vectors_dataframe)

# define tsne model with given perplexity, learning_rate
tsne_model = TSNE(perplexity=num_perplexity, learning_rate=num_learning_rate)

# fit t-sne model, dimensional reduction
fitted_model_2d = tsne_model.fit_transform(rm_dw_member_vectors_dataframe.data)

# Plotting 2-dimensional t-sne
y_axis = fitted_model_2d[:, 1]
x_axis = fitted_model_2d[:, 0]

plt.figure(1)
plt.scatter(x_axis, y_axis, c=member_vectors_dataframe[:,13],cmap='bwr')

plt.figure(2)
member_vectors_data_2 = np.column_stack((x_axis, y_axis))

# declare tsne plot for k-means clustering
k_means_model = KMeans(n_clusters=cluster_optimization)

# fit k-means model
k_means_model.fit(member_vectors_data_2)

# color-code points pased on predictions
all_predictions = k_means_model.predict(member_vectors_data_2)
# print(all_predictions)

plt.scatter(x_axis, y_axis, c=all_predictions)

# plt.show()

# fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)
# # declare t-sne plot for dw-nominate clustering
# # utilize dw-nominated for color gradient
# axs[0].scatter(x_axis, y_axis, c=member_vectors_dataframe[:,13], cmap='bwr')
# # declare tsne plot for k-means clustering
# axs[1].scatter(x_axis, y_axis, c=all_predictions)
#
# names = member_vectors_dataframe[:,15]
# print(names)

info_vect = []

with open('candidate_info.csv') as csv_file_2:
    csv_reader = csv.reader(csv_file_2)
    for row in csv_reader:
        arr = []
        for i in range(len(row)):
            if i == 3:
                if row[i][2:-1] == 'S':
                    arr[1] = arr[1] + ' (S)'
                else:
                    arr[1] = arr[1] + ' (H)'
                arr.append(regions.get(row[i][:-2]))
            elif i == 7:
                # print(row[i])
                if row[i] == 'F':
                    arr.append(1)
                if row[i] == 'M':
                    arr.append(2)
            else:
                arr.append(row[i])

        info_vect.append(arr)

print(info_vect)

name = 1
region = 3
biggest_sector = 5
second_sector = 6
gender = 7

def column(matrix, i):
    return [row[i] for row in matrix]

labels = column(info_vect,name)

for label, x, y in zip(labels, x_axis, y_axis):
    plt.annotate(
        label,
        xy=(x, y), xytext=(-2, 2),
        textcoords='offset points')

labels = column(info_vect,region)
region_map = {'s':1,'n':2,'c':3,'w':4}

for i in range(len(labels)):
    labels[i] = region_map.get(labels[i])

plt.figure(3)
plt.scatter(x_axis, y_axis, c=labels)

labels = column(info_vect,biggest_sector)

plt.figure(4)
plt.scatter(x_axis, y_axis, c=list(map(int, labels)),cmap='Paired')

plt.figure(5)
plt.scatter(x_axis, y_axis, c=all_predictions)


labels = column(info_vect,second_sector)
plt.figure(6)
plt.scatter(x_axis, y_axis, c=list(map(int, labels)),cmap='Paired')

labels = column(info_vect,gender)
plt.figure(7)
plt.scatter(x_axis, y_axis, c=labels,cmap='Accent')

# show both plots
plt.show()
