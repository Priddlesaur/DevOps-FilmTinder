from dataset import users, movies, ratings

if __name__ == "__main__":
    users.populate_users()
    movies.populate_movies()
    ratings.populate_ratings()
    print("Users and movies populated")
