from fastapi import APIRouter, Response

from dataset import users, movies, ratings

router = APIRouter(
    prefix="/actions",
    tags=["actions"],
)

@router.get("/populate")
async def populate_database():
    users.populate_users()
    movies.populate_movies()
    ratings.populate_ratings()
    return Response(status_code=201, content="Users, movies and ratings populated")
