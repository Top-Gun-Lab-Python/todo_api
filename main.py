from fastapi import FastAPI, status, HTTPException
from database import Base, engine, Todo
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Create the database
Base.metadata.create_all(engine)

app = FastAPI()

# Create Read Update Delete
@app.get("/")
def root():
    return "todo"

class ToDoRequest(BaseModel):
    task: str

# Create
@app.post("/todo")
def create_todo(todo: ToDoRequest):

    # crate database session
    session = Session(bind=engine, expire_on_commit=False)

    # create instane of the ToDo database model
    tododb = Todo(task = todo.task)

    session.add(tododb)
    session.commit()

    # getting the created task id
    id = tododb.id
    # closing the session
    session.close()

    return { "id":id, "task": todo.task}



# Read
@app.get("/todo/{id}")
def read_todo(id: int):
    
    # crate database session
    session = Session(bind=engine, expire_on_commit=False)

    todo = session.query(Todo).get(id) # SELECT * FROM todos WHERE ID = 1

    session.close()

    if not todo:
        raise HTTPException(status_code, detail=f"todo item whit id {id} not found")

    return { "id": todo.id, "task": todo.task}

# Update
@app.put("/todo/{id}")
def update_todo(id: int, task: str):
    session = Session(bind=engine, expire_on_commit=False)

    todo = session.query(Todo).get(id)

    if todo:
        todo.task = task
        session.commit()

    session.close()

    if not todo:
        raise HTTPException(status_code, detail=f"todo item whit id {id} not found")

    return todo

# Delete
@app.delete("/todo/{id}")
def delete_todo(id: int):
    session = Session(bind=engine, expire_on_commit=False)

    todo = session.query(Todo).get(id)

    if todo:
        session.delete(todo)
        session.commit()

    session.close()

    if not todo:
        raise HTTPException(status_code, detail=f"todo item whit id {id} not found")

    return todo

# Get ALL
@app.get("/todo")
def read_todo_list():
        # crate database session
    session = Session(bind=engine, expire_on_commit=False)

    todo_list = session.query(Todo).all() # SELECT * FROM todos

    session.close()

    return todo_list
