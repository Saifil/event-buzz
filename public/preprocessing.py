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

EMBEDDING_NAME = 'bert/embeddings'

try:
    embeddings = np.load(EMBEDDING_NAME + '.npy')
    # print("Saved embeddings found")
    # print(embeddings.shape)

except FileNotFoundError:  # will not work as there is no output.jsonl in this directory
    print("Saved embeddings not found: Creating embeddings")
    with open("bert/output.jsonl") as fp:
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

kmeans = KMeans(n_clusters=20, random_state=0).fit(embeddings)
# print(f"K-means labels: {kmeans.labels_}, label-size: {kmeans.labels_.shape}")


x = kmeans.labels_
unique, counts = np.unique(x, return_counts=True)

# print(np.asarray((unique, counts)).T)

try:
    test_embeddings = np.load("bert/embeddings_main" + '.npy')
except FileNotFoundError:
    print("Test embedding npt found: file bert/embeddings_main.npy doesn't exits")
    exit(0)

prediction = kmeans.predict(test_embeddings)
# print(prediction)

cluster_number = 0


def analyse_clusters():
    with open("output/input.txt") as fp:
        line = fp.readline()
        i = 0
        while line:
            per_list = line.strip()
            if prediction[i] == cluster_number:
                print(per_list)
            line = fp.readline()
            i += 1


analyse_clusters()
#
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
# get all events in cluster 1


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
