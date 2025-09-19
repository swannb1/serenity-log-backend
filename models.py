from sqlmodel import Field, Relationship, SQLModel

class Entry(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    post: str
    mood: int
    # tags: list[str] | None = None
    date: str
    user_username: str = Field(foreign_key="users.username", index=True)
    users: "Users" | None = Relationship(back_populates="entries")

class Users(SQLModel, table=True):
    username: str = Field(primary_key=True, index=True)
    full_name: str
    email: str
    hashed_password: str
    token: str | None = None
    entries: list[Entry] = Relationship(back_populates="users")

