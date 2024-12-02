from dataset import users, movies

if __name__ == "__main__":
    users.populate_users()
    movies.populate_movies()
    print("Users and movies populated")
