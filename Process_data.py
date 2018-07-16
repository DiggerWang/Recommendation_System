import pandas as pd
import numpy as np
import scipy.io as scio

#处理movies.dat
def process_movies():
    movies = open('Data/movies.csv').readlines()
    file = open('movies.txt','w')
    for i in movies[1:]:
        a = i.split(",")
        file.write(a[0]+'.'+a[1]+'\n')
    file.close()


#处理ratings.dat
def process_ratings():
    ratings = open('Data/ratings.csv').readlines()
    movies = open('Data/movies.csv').readlines()
    movie_list = []
    for i in movies[1:]:
        x = i.split(",")
        movie_list.append(x[0])
    rating_matrix = np.zeros([9126,671])
    R_matrix = np.zeros([9126,671])
    for i in ratings[1:]:
        a = i.split(",")
        b = movie_list.index(a[1])
        try:
            rating_matrix[b, int(a[0])-1] = float(a[2])
            R_matrix[b, int(a[0])-1] = 1
        except:
            print(b)
    scio.savemat('ratings.mat', {'Y':rating_matrix, 'R':R_matrix})


if __name__ == '__main__':
    process_ratings()
