from cogs.lastfm_cog import get_top_artists
from similarities import *

def compare_ulv_and_joh():
    print(compare_users("RollTheBones67", "reddituser0"))
    
    top_artist_dict_ulv = get_top_artists("appellation1")
    top_artist_dict_joh = get_top_artists("RollTheBones67")
    top_artists_ulv = set(top_artist_dict_ulv.keys())
    top_artists_joh = set(top_artist_dict_joh.keys())
    shared_artists = top_artists_ulv.intersection(top_artists_joh)
    for artist in shared_artists:
        print(artist + "\n" + str(top_artist_dict_ulv[artist]) + "\t" +
              str(top_artist_dict_joh[artist]))
    


if __name__ == "__main__":
    compare_ulv_and_joh()