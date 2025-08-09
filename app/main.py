#library mangement
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine, Base
from app.models import item_model
from app.schemas.item_schema import ItemSchema
from app.crud import item_crud

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items")
def create_item(item: ItemSchema, db: Session = Depends(get_db)):
    return item_crud.create_item(db, item)

@app.get("/items")
def read_items(db: Session = Depends(get_db)):
    return item_crud.get_all_items(db)

@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = item_crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}")
def update(item_id: int, item: ItemSchema, db: Session = Depends(get_db)):
    updated = item_crud.update_item(db, item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

@app.delete("/items/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    deleted = item_crud.delete_item(db, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted", "deleted_item": deleted}
