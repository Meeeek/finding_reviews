# Conrad Fukuzawa
# August 2020

import web_nav
import time

# Steps to follow
#     1. find website
#     2. use browser things to search
#     3. figure out link from first option
# Websites
#     1. rotten tomatoes
#     2. imdb
#     3. metacritic (REDACTED)
# Issues
#     1. Handling bad stuff from rotten tomatoes

def main():
    name = input("What movie?\n")
    direc = '' # NOT IMPLEMENETED
    mov1 = {}
    mov2 = {}
    mov3 = {}

    # TEMP CODE ------------
    mov1['rating'] = 50
    mov2['rating'] = 50
    mov3['rating'] = 50
    # This is so that the code doesn't break when showing stats
    # TEMP CODE ENDS --------
    
    # Getting movie info from Rotten Tomatoes
    rot = web_nav.Rotten(name, direc)
    mov1 = rot.get_movie()
    rot.close()

    # Getting movie info from IMDB
    imdb = web_nav.Imdb(name, direc)
    mov2 = imdb.get_movie()
    imdb.close()

    # Getting movie info from metacritic METACRITIC BLOCKS
    # meta = web_nav.Meta(name, direc)
    # mov2 = meta.get_movie()
    # meta.close()

    # SHOWING STATS ---------------------------------------------
    avg = (mov1['rating'] + mov2['rating']) / 2
    print("############################")
    print(f"Rotten Tomatoes: {mov1}")
    print(f"IMDB: {mov2}")
    #print(f"Metacritic: {mov3}")
    print("############################")
    print(f"average is {avg}")


if __name__=='__main__':
    tim1 = time.clock()
    main()
    print('---------------------------------------')
    print(f'time passed is {time.clock() - tim1}')
