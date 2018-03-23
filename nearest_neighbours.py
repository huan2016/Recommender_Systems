from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import io  # needed because of weird encoding of u.item file

from surprise import KNNBaseline
from surprise import Dataset
from surprise import get_dataset_dir


def read_item_names():
    """Read the u.item file from MovieLens 100-k dataset and return two
    mappings to convert raw ids into movie names and movie names into raw ids.
    """

    file_name = get_dataset_dir() + '/ml-100k/ml-100k/u.item'
    rid_to_name = {}
    name_to_rid = {}
    with io.open(file_name, 'r', encoding='ISO-8859-1') as f:
        for line in f:
            line = line.split('|')
            rid_to_name[line[0]] = line[1]
            name_to_rid[line[1]] = line[0]

    return rid_to_name, name_to_rid


# First, train the algortihm to compute the similarities between items
data = Dataset.load_builtin('ml-100k')
trainset = data.build_full_trainset()
sim_options = {'name': 'pearson_baseline', 'user_based': False}
algo = KNNBaseline(sim_options=sim_options)
algo.fit(trainset)

# Read the mappings raw id <-> movie name
rid_to_name, name_to_rid = read_item_names()

# Retrieve inner id of the movie
movie_raw_id = name_to_rid['Clockwork Orange, A (1971)']
movie_inner_id = algo.trainset.to_inner_iid(movie_raw_id)
movie_neighbors = algo.get_neighbors(movie_inner_id, k=10)

# Convert inner ids of the neighbors into names.
movie_neighbors = (algo.trainset.to_raw_iid(inner_id)
                   for inner_id in movie_neighbors)
movie_neighbors = (rid_to_name[rid]
                   for rid in movie_neighbors)

print()
print('The 10 nearest neighbors of Toy Story are:')
for movie in movie_neighbors:
    print(movie)
