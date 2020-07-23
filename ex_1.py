# Stav Koren 207128539
import sys
from math import sqrt, hypot
import scipy.io.wavfile
import numpy as np


# the function compute the distance between two points
def distance_between_two_points(p1x, p1y, p2x, p2y):
    return hypot(p1x - p2x, p1y - p2y)


# the function classifies each point to the nearest centroid
def classify_point_to_centroid_index(all_points, current_centroids):
    current_points_centroid = []
    # for each point
    for point in all_points:
        distances = list()
        # calculate distance for point to each centroid
        for current_centroid in current_centroids:
            distances.append(distance_between_two_points(point[0], point[1], current_centroid[0], current_centroid[1]))
        # append the index of the nearset centroid
        current_points_centroid.append(distances.index(min(distances)))
    return current_points_centroid;


sample, centroid = sys.argv[1], sys.argv[2]
fs, y = scipy.io.wavfile.read(sample)
points = np.array(y.copy())
centroids = np.loadtxt(centroid)
k = len(centroids)
iterations = 0
old_centroids = []
f = open("output.txt", "w+")
while iterations < 30 and not np.array_equal(centroids, old_centroids):
    # classify each point to centroid
    points_classifications = classify_point_to_centroid_index(points, centroids)
    # update centroids
    old_centroids = centroids.copy()
    for centroid_index in range(0, len(centroids)):
        sum_x = 0
        sum_y = 0
        count_points_classify = 0
        for i in range(0, len(points_classifications)):
            # if the current point belong to the current centroid
            if centroid_index == points_classifications[i]:
                count_points_classify += 1
                sum_x += points[i][0];
                sum_y += points[i][1];
            i += 1
        if count_points_classify > 0:
            # calculate new centroid
            x_mean = round(sum_x / count_points_classify)
            y_mean = round(sum_y / count_points_classify)
            centroids[centroid_index][0] = x_mean
            centroids[centroid_index][1] = y_mean
        centroid_index += 1
    print(f"[iter {iterations}]:{','.join([str(j) for j in centroids])}")
    f.write(f"[iter {iterations}]:{','.join([str(j) for j in centroids])}")
    f.write("\n")
    iterations += 1
