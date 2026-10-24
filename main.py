from fastapi import FastAPI, Depends, HTTPException
from schemas import Todo as TodoSchema, TodoCreate
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Todo
from database import Base, engine
Base.metadata.create_all(bind = engine) 

app = FastAPI()



# Dependency for DB Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# POST - Create Todo
@app.post('/todos', response_model=TodoCreate)
def create(todo: TodoCreate, db: Session=Depends(get_db)):
    db_todo = Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# GET - Fetch ALL
@app.get('/todos', response_model=list[TodoCreate])
def get_all(db: Session=Depends(get_db)):
    return db.query(Todo).all()

# GET one by Id
@app.get('/todo/{todo_id}', response_model=TodoSchema)
def read_todo(todo_id: int, db: Session=Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail='Todo not found')
    return todo

# PUT Update by id
@app.put('/todo/{todo_id}', response_model=TodoSchema)
def update_todo(todo_id: int, updated: TodoCreate, db: Session=Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail='Todo not found')
    for key, value in updated.dict().items():
        setattr(todo, key, value)
    db.commit()
    db.refresh(todo)
    return todo


# DELETE dele by id
@app.delete('/todo/{todo_id}', response_model=TodoSchema)
def delete_todo(todo_id: int, db:Session=Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail='Todo not found')
    db.delete(todo)
    db.commit()
    return {'message':'Todo deleted successfully'}
