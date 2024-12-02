from fastapi import HTTPException
from sqlalchemy.orm import Session

def delete_or_rollback(instance: object, db: Session):
    try:
        db.delete(instance)
        db.commit()
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=400, detail="An error occurred while deleting the genre")
