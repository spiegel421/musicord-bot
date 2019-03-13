import copy
import math
import numpy
from collections import defaultdict
from cogs.lastfm_cog import get_top_artists
from data import lastfm_data
from pandas import DataFrame
from sklearn.decomposition import TruncatedSVD

NUM_FEATURES = 500
NUM_TOP_FEATURES = 100


def gen_user_artist_dataframe():
    """Create a matrix with users as rows and artists as columns,
       corresponding to each user's playcount of each artist"""
    print("Generating dataframe from lastfm usernames.")
    user_to_id_dict = lastfm_data.get_users_and_ids()
    playcounts = defaultdict(dict)
    users = user_to_id_dict.keys()
    count = 0
    for user in users:
        count += 1
        top_artist_dict = get_top_artists(user)
        top_artists = top_artist_dict.keys()
        for artist in top_artists:
            playcounts[user][artist] = top_artist_dict[artist]
        print(str(count) + "/" + str(len(users)) + " users counted.")

    df = DataFrame(playcounts).T.fillna(0.0)
    return df


def gen_ppmi_dataframe(df):
    """Generate a ppmi value for each user and artist"""
    print("Finding ppmi values.")
    total_playcount = sum(df.sum())
    user_playcounts = df.sum(axis=1)
    artist_playcounts = df.sum(axis=0)
    ppmi_df = copy.copy(df)
    count = 0
    for user, user_artist_playcounts in df.iterrows():
        count += 1
        for artist in user_artist_playcounts.index:
            user_artist_playcount = user_artist_playcounts[artist]
            if user_artist_playcount == 0.0:
                ppmi = 0.0
            else:
                x = total_playcount * user_artist_playcount
                y = user_playcounts[user] * artist_playcounts[artist]
                ppmi = max(0.0, x / y)
            ppmi_df.at[user, artist] = ppmi
        print(str(count) + "/" + str(len(user_playcounts)) + " users counted.")

    return ppmi_df


def scale(ppmi_df):
    svd = TruncatedSVD(n_components=NUM_FEATURES, algorithm="randomized",
                       n_iter=1)
    reduced = svd.fit_transform(ppmi_df)
    return DataFrame(reduced, index=ppmi_df.index)


def find_similarities(ppmi_df):
    """Find Pearson correlation coefficients between all users"""
    def top_features(vector, N):
        indices = [i for i in range(len(vector))]
        dict_vector = dict(zip(indices, vector))
        top_features = sorted(dict_vector.keys(),
                              key=lambda x: dict_vector[x],
                              reverse=True)
        return top_features[:N]
        
    def APSyn(vectorA, vectorB):
        sim = 0.0
        top_featuresA = top_features(vectorA, NUM_TOP_FEATURES)
        top_featuresB = top_features(vectorB, NUM_TOP_FEATURES)
        intersect = set(top_featuresA).intersection(set(top_featuresB))
        for f in intersect:
            rankA = top_featuresA.index(f) + 1
            rankB = top_featuresB.index(f) + 1
            avg = (rankA + rankB) / 2
            sim += 1 / avg
        return sim
        

    print("Finding similarities.")
    users = ppmi_df.index
    similarities = defaultdict(dict)
    count = 0
    for userA in users:
        count += 1
        vectorA = ppmi_df.loc[userA]
        for userB in users:
            vectorB = ppmi_df.loc[userB]
            similarities[userA][userB] = APSyn(vectorA, vectorB)

        print(str(count) + "/" + str(len(users)) + " users counted.")

    return similarities


def record_similarities(similarities):
    """Record user similarities to text file"""
    writer = open("similarities.txt", "w")
    for userA in similarities.keys():
        for userB in similarities[userA].keys():
            writer.write(userA + "\t" + userB + "\t" +
                         str(similarities[userA][userB]) + "\n")
    writer.close()


def sort_similarities():
    """Given a similarities file, sort the similarities from high to low"""
    reader = open("similarities.txt", "r")
    lines = reader.readlines()
    sims_ranked = list()
    for line in lines:
        a, b, sim = line.split("\t")
        sims_ranked.append(float(sim))

    sims_ranked = sorted(sims_ranked, reverse=True)
    writer = open("sorted_similarities.txt", "w")
    for sim in sims_ranked:
        writer.write(str(sim) + "\n")


def compare_users(userA, userB):
    """Find the percentile similarity between two users"""
    reader = open("similarities.txt", "r")
    lines = reader.readlines()
    similarity = None
    for line in lines:
        a, b, sim = line.split("\t")
        if userA == a and userB == b:
            print(sim)
            similarity = float(sim)

    reader2 = open("sorted_similarities.txt", "r")
    lines = reader2.readlines()
    index = 0.0
    for line in lines:
        sim = float(line)
        if similarity == sim:
            return 1.0 - (float(index) / len(lines))
        index += 1

    return None
            
    
    """
    if len(sim_dict.keys()) == 0:
        return None

    ranked = sorted(sim_dict.keys(), key=lambda x: sim_dict[x],
                    reverse=True)
    try:
        index = ranked.index(userB)
        percentile = 1.0 - (float(index) / len(sim_dict.keys()))
        return int(100 * percentile)
    except:
        return None
    """


def most_similar(user):
    """Find 10 most similar users to given user"""
    reader = open("similarities.txt", "r")
    lines = reader.readlines()
    sim_dict = dict()
    for line in lines:
        a, b, sim = line.split("\t")
        if user == a:
            sim_dict[b] = float(sim)

    if len(sim_dict.keys()) == 0:
        return None

    ranked = sorted(sim_dict.keys(), key=lambda x: sim_dict[x],
                    reverse=True)

    return ranked[1:13]


def obscurity(user):
    """Find average similarity of user"""
    reader = open("similarities.txt", "r")
    lines = reader.readlines()
    obscurity = 0.0
    count = 0
    for line in lines:
        a, b, sim = line.split("\t")
        if user == a:
            count += 1
            obscurity += float(sim)

    obscurity /= count
    return obscurity


def rank_by_obscurity():
    """Rank all users by obscurity"""
    obscurities = dict()
    reader = open("similarities.txt", "r")
    lines = reader.readlines()
    for line in lines:
        a, b, sim = line.split("\t")
        if a not in obscurities:
            obscurities[a] = [float(sim), 1.0]
        else:
            obscurities[a] = [obscurities[a][0] + float(sim),
                              obscurities[a][1] + 1.0]
            
    ranked = sorted(obscurities.keys(),
                    key=lambda x: obscurities[x][0] / obscurities[x][1])
    writer = open("obscurities.txt", "w")
    for user in ranked:
        writer.write(user + "\n")


def main():
    """Run the script to generate pairwise similarities"""
    # Test code.
    #books = {}
    #books['hi'] = {'ffa': 1, 'gerjk': 40, 'eqrwf': 5}
    #books['bye'] = {'ffa': 30, 'grahooe': 4, 'ghuiewq': 2, 'fw': 10}
    #books['x'] = {'ffa': 40}
    #df = DataFrame(books).T.fillna(0)
    
    df = gen_user_artist_dataframe()
    ppmi_df = gen_ppmi_dataframe(df)
    ppmi_df = scale(ppmi_df)
    similarities = find_similarities(ppmi_df)
    record_similarities(similarities)


if __name__ == "__main__":
    main()