from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

def get_all_entities(entity_class, db: Session):
    """
    Helper function that retrieves all entities from the provided data.
    """
    return db.query(entity_class).all()

def get_entity(entity_class, entity_id: int, db: Session):
    """
    Helper function that retrieves an entity from the provided data by its ID.
    """
    entity = db.get(entity_class, entity_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    return entity

def create_or_rollback(entity_class, entity_data: dict, db: Session):
    """
    Helper function to create an entity in the database using the provided data.
    Some classes include foreign keys, which may raise exceptions in some cases.
    """
    new_entity = entity_class(**entity_data)

    for field, value in entity_data.items():
        expect_type = getattr(entity_class, field).type.python_type
        if not isinstance(value, expect_type) and value is not None:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Invalid type input: Field {field} must be of type {expect_type}")

    try:
        db.add(new_entity)
        db.commit()
        db.refresh(new_entity)
    except IntegrityError as err:
        db.rollback()
        if "foreign key constraint" in str(err.orig).lower():
            raise HTTPException(status_code=400, detail="Invalid foreign key value")
        raise HTTPException(status_code=400, detail="Database constraint error")
    except KeyError as err:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Invalid field: {str(err)}")
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    return new_entity

def update_or_rollback(instance: object, updates: dict, db: Session):
    """
    Helper function that updates an entity from the provided data by its ID.
    Some classes include foreign keys, which may raise exceptions in some cases.
    """
    if not updates:
        raise HTTPException(status_code=400, detail="No valid fields for update")

    for key,value in updates.items():
        expect_type = getattr(instance.__class__, key).type.python_type
        if not isinstance(value, expect_type) and value is not None:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Invalid type input: Key {key} must be of type {expect_type}")
        setattr(instance, key, value)

    try:
        db.commit()
        db.refresh(instance)
    except IntegrityError as err:
        db.rollback()
        if "foreign key constraint" in str(err.orig).lower():
            raise HTTPException(status_code=400, detail="Invalid foreign key value")
        raise HTTPException(status_code=400, detail="Database constraint error")
    except KeyError as err:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Invalid field: {str(err)}")
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    return instance

def delete_or_rollback(instance: object, db: Session):
    """
    Helper function that deletes an entity by its ID.
    """
    try:
        db.delete(instance)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="An error occurred while deleting")



