from flask import Flask,jsonify
import csv
from Storage import all_movies,liked_movies,not_liked_movies,not_watched_movies
from Demographic_Filter import output
from Content_Filter import get_reccomendations

app = Flask(__name__)
@app.route("/get-movie")

def get_movie():
    movie_data = {
        "title": all_movies[0][19], 
        "poster_link": all_movies[0][27], 
        "release_date": all_movies[0][13] or "N/A", 
        "duration": all_movies[0][15], 
        "rating": all_movies[0][20], 
        "overview": all_movies[0][9],
    }
    return jsonify({
        "data" : movie_data,
        "status" : "success"
    })

@app.route("/liked-movie",methods=["POST"])

def liked_movie():
    movie = all_movies[0]
    all_movies = all_movies[1:]
    liked_movies.append(movie)
    return jsonify({
        "status" : "success",
    }),201

@app.route("/not-liked-movie",methods=["POST"])

def not_liked_movie():
    movie = all_movies[0]
    all_movies = all_movies[1:]
    not_liked_movies.append(movie)
    return jsonify({
        "status" : "success",
    }),201

@app.route("/not-watched-movie",methods=["POST"])

def not_watched_movie():
    movie = all_movies[0]
    all_movies = all_movies[1:]
    not_watched_movies.append(movie)
    return jsonify({
        "status" : "success",
    }),201

@app.route("/popular_movies")

def popular_movies():
    movie_data = []
    for movie in output:
        d = {
            "title": movie[0], 
            "poster_link": movie[1], 
            "release_date": movie[2] or "N/A", 
            "duration": movie[3], 
            "rating": movie[4], 
            "overview": movie[5]
        }
        movie_data.append(d)
    return jsonify({
        "data" : movie_data,
        "status" : "success",
    }),200

@app.route("/recommended_movies")

def recommended_movies():
    all_recommended = []
    for liked_movie in liked_movies:
        output = get_reccomendations(liked_movie[19])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    movie_data = []
    for recommended in all_recommended:
        d = {
            "title": recommended[0], 
            "poster_link": recommended[1], 
            "release_date": recommended[2] or "N/A", 
            "duration": recommended[3], 
            "rating": recommended[4], 
            "overview": recommended[5]
        }
        movie_data.append(d)
    return jsonify({
        "data" : movie_data,
        "status" : "success",
    }),200

if __name__=="__main__":
    app.run()