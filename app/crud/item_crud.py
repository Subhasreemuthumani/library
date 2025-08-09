from sqlalchemy.orm import Session
from app.models.item_model import Item
from app.schemas.item_schema import ItemSchema

def create_item(db: Session, item: ItemSchema):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def get_all_items(db: Session):
    return db.query(Item).all()

def update_item(db: Session, item_id: int, item_data: ItemSchema):
    db_item = get_item(db, item_id)
    if db_item:
        db_item.name = item_data.name
        db_item.price = item_data.price
        db.commit()
        db.refresh(db_item)
        return db_item
    return None

def delete_item(db: Session, item_id: int):
    db_item = get_item(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
