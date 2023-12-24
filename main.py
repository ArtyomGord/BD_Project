import model
import sessions
from fastapi import FastAPI, HTTPException, status
from fastapi import Query

SESSION = sessions.connect_to_session()

def create_BD():
    engine = sessions.connect_to_base()
    model.BASE.metadata.create_all(engine)

if __name__ == "__main__":
    create_BD()

