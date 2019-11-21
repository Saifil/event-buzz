import json
import numpy as np
from sklearn.cluster import KMeans
import matplotlib

matplotlib.use("TKAgg")
import matplotlib.pyplot as plt

import database.data.mongo_setup as mongo_setup
import database.services.data_service as svc
import database.infrastructure.state as state

from database.data.event import Event

################START

# EMBEDDING_NAME = 'bert/embeddings'
EMBEDDING_NAME = 'bert/embeddings_clean'

try:
    embeddings = np.load(EMBEDDING_NAME + '.npy')
    # print("Saved embeddings found")
    # print(embeddings.shape)

except FileNotFoundError:  # will not work as there is no output.jsonl in this directory
    print("Saved embeddings not found: Creating embeddings")
    # with open("bert/output.jsonl") as fp:
    with open("bert/output_clean.jsonl") as fp:
        line = fp.readline()

        embeddings = []
        while line:
            per_line_layer_2 = []
            jsn_line = json.loads(line.strip())
            for jsn_features in jsn_line['features']:  # for each word in the line
                per_line_layer_2.append(jsn_features['layers'][1]['values'])  # appends the list for layer 2
            embeddings.append(np.mean(np.asarray(per_line_layer_2), axis=0))
            line = fp.readline()

        embeddings = np.asarray(embeddings)
        print(embeddings.shape)

        np.save(EMBEDDING_NAME, embeddings)  # save the file as "outfile_name.npy"

kmeans = KMeans(n_clusters=50, random_state=0).fit(embeddings)
# print(f"K-means labels: {kmeans.labels_}, label-size: {kmeans.labels_.shape}")
prcts = kmeans.labels_
# print(prcts.shape)

# x = kmeans.labels_
# unique, counts = np.unique(x, return_counts=True)

# print(np.asarray((unique, counts)).T)
#
#
# def find_matchings(cluster_number):
#     with open("output/input.txt") as fp:
#         # print(f"Cluster number: {cluster_number}")
#         line = fp.readline()
#         i = 0
#         while line:
#             per_list = line.strip()
#             if prcts[i] == cluster_number:
#                 print(per_list)
#             line = fp.readline()
#             i += 1


#########here
#
# def find_matchings(cluster_number):
#     file = open("output/clusters/cluster_clean_unnumbered/clstr_" + str(cluster_number) + ".txt", 'a+')
#     # file = open("output/clusters/cluster_" + str(cluster_number) + ".txt", 'a+')
#     with open("output/input.txt") as fp:
#         print(f"Cluster number: {cluster_number}")
#         line = fp.readline()
#         i = 0
#         while line:
#         # while line:
#             per_list = line.strip()
#             if prcts[i] == cluster_number:
#                 # print(per_list)
#                 file.write(per_list + "\n")
#             line = fp.readline()
#             i += 1
#     file.close()
#
# for i in range(50):
#     find_matchings(i)

# try:
#     test_embeddings = np.load("bert/embeddings_main" + '.npy')
# except FileNotFoundError:
#     print("Test embedding npt found: file bert/embeddings_main.npy doesn't exits")
#     exit(0)
#
# prediction = kmeans.predict(test_embeddings)

################END

#
# # embedding = np.load('bert/embeddings_main.npy')
# embedding = np.load('bert/embeddings_main.npy')
# training = embedding[:embedding.shape[0] - 50, :]
# testing = embedding[embedding.shape[0] - 50:, :]
# kmean = KMeans(n_clusters=50, random_state=0).fit(training)
#
# pred = kmean.predict(testing)
# print(pred)
#
# prediction = kmean.labels_
#
# # mongo_setup.global_init()  # Connect to the db
#
# # print(prediction)
#
# # cluster_number = 4
# #
# #
# def analyse_clusters(cluster_number):
#     file = open("output/clusters/cluster_old/cluster_" + str(cluster_number) + ".txt", 'a+')
#     # file = open("output/clusters/cluster_" + str(cluster_number) + ".txt", 'a+')
#     with open("output/input.txt") as fp:
#         print(f"Cluster number: {cluster_number}")
#         line = fp.readline()
#         i = 0
#         while line and i < prediction.shape[0]:
#         # while line:
#             per_list = line.strip()
#             if prediction[i] == cluster_number:
#                 # print(per_list)
#                 file.write(per_list + "\n")
#             line = fp.readline()
#             i += 1
#     file.close()
#
#
# def generate_test_file_description():
#     j = 0
#     file = open("output/clusters/cluster_old/test/cluster_test.txt", 'a+')
#     with open("output/input.txt") as fp:
#         line = fp.readline()
#         i = 0
#         while line:
#             per_list = line.strip()
#             if i >= embedding.shape[0] - 50:
#                 file.write(str(pred[j]) + ":" + str(i) + "\n")
#                 j += 1
#             line = fp.readline()
#             i += 1
#     file.close()
#
#
#
# # for i in range(0, 50):
# #     analyse_clusters(i)
#
# generate_test_file_description()

# def init_connection_to_mongo():
#     mongo_setup.global_init()  # Connect to the db
#
#
# def assign_clusters_to_events():
#     i = 0
#     for event in Event.objects():
#         event.update(set__cluster_number=int(kmeans.labels_[i]))
#         i += 1
#
# # DO NOT CALL UNLESS NECESSARY
# init_connection_to_mongo()
#
# assign_clusters_to_events()


##########################
# distorsions = []
# scores = []
# nc = range(2, 20)
# for k in nc:
#     print(k)
#     kmeans = KMeans(n_clusters=k, random_state=0)
#     kvar = kmeans.fit(embeddings)
#     distorsions.append(kmeans.inertia_)
#     # scores.append(kvar.score(embeddings))
#     scores.append(kvar.score(embeddings))
#
#
# fig = plt.figure()
# plt.plot(nc, distorsions)
# plt.ylabel("Sqaured Error (Cost)")
# plt.xlabel("Number of Clusters")
# plt.grid(True)
# plt.title('Elbow curve')
# plt.show()
##########################

#
# distorsions = []
# nc = range(1, 10)
# kmeans = [KMeans(n_clusters=i) for i in nc]
# print("========Calculated k-means========")
#
# fitted = [kmeans[i].fit(embeddings) for i in range(len(kmeans))]
# print("========Fitted k-means========")
#
# distorsions.append(kmeans[i].inertia_ for i in range(len(kmeans)))
# print("========Calculated k-means Distortions========")
#
# score = [fitted[i].score(embeddings) for i in range(len(fitted))]
# print("========Scored k-means========")


# fig = plt.figure(figsize=(15, 5))
# plt.plot(nc, score)
# plt.grid(True)
# plt.xlabel("Number of clusters")
# plt.ylabel("Score")
# plt.title("Elbow curve")
# plt.show()
# fig.show()
#
# print("========Plotting elbow graphs========")
#
# fig_sub = plt.figure()
#
# plt.subplot(2, 1, 1)
# plt.plot(nc, scores)
# plt.grid(True)
# plt.xlabel("Number of clusters")
# plt.ylabel("Score")
# plt.title("Elbow curve")
#
# plt.subplot(2, 1, 2)
# plt.plot(nc, distorsions)
# plt.ylabel("Sqaured Error (Cost)")
# plt.xlabel("Number of Clusters")
# plt.grid(True)
# plt.title('Elbow curve (Distortions)')
#
# fig_sub.tight_layout()
# fig_sub.savefig("output/elbow.png")
