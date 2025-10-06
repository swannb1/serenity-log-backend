from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, func, desc

from database import get_db
from models import Entry, EntryTagLink, Tag, Users
from schemas import CreateUserRequest, CreateEntryRequest, Token, TokenData
from utils.security import authenticate_user, create_access_token, get_current_user, hash_password, verify_password


from routers import ai, auth
from fastmcp import FastMCP

app = FastAPI(title="<rAIos>")
router = APIRouter()
# Create an MCP server based on this app

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(ai.router, prefix="/ai", tags=["ai"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:8080/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

###USERS###
@router.get("/users", tags=["Users"])
async def get_users(db: Session = Depends(get_db)) -> list[Users]:
    return db.exec(select(Users)).all()

@router.post("/users", status_code=status.HTTP_201_CREATED, tags=["Users"])
async def create_user(new_user: CreateUserRequest, db: Session = Depends(get_db)) -> None:
    hashed_password: str = hash_password(new_user.password)
    user: Users = Users(**new_user.model_dump(), hashed_password=hashed_password)
    db.add(user)
    db.commit()

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
async def delete_user(user_id: int, db: Session = Depends(get_db)) -> None:
    user: Users | None = db.get(Users, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    db.delete(user)
    db.commit()

###ENTRIES###
@router.get("/entry", tags=["Entries"], operation_id="get_entries")
async def get_entries(db: Session = Depends(get_db)) -> list[Entry]:
    return db.exec(select(Entry)).all()

@router.post("/entry", status_code=status.HTTP_201_CREATED, tags=["Entries"], operation_id="create_entry")
async def create_entry(new_entry: CreateEntryRequest, db: Session = Depends(get_db)) -> None:
    entry: Entry = Entry(**new_entry.model_dump())
    db.add(entry)
    db.commit()

@router.delete("/entry/{entry_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Entries"])
async def delete_entry(entry_id: int, db: Session = Depends(get_db)) -> None:
    entry: Entry | None = db.get(Entry, entry_id)
    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Entry with id {entry_id} not found")
    db.delete(entry)
    db.commit()

app.include_router(router)

mcp = FastMCP.from_fastapi(app=app)

if __name__ == "__main__":
    mcp.run()

