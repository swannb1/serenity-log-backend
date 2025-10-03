from sqlmodel import Field, Relationship, SQLModel

class EntryTagLink(SQLModel, table=True):
    entry_id: int | None = Field(foreign_key="entry.id", primary_key=True)
    tags_id: int | None = Field(foreign_key="tag.id", primary_key=True)

class Entry(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    post: str
    mood: int
    tags: list['Tag'] = Relationship(back_populates="entries", link_model=EntryTagLink)
    date: str
    user_username: str = Field(foreign_key="users.username", index=True)
    users: 'Users' = Relationship(back_populates="entries")

class Users(SQLModel, table=True):
    username: str = Field(primary_key=True, index=True)
    full_name: str
    email: str
    hashed_password: str
    token: str | None = None
    entries: list[Entry] = Relationship(back_populates="users")

class Tag(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    content: str = Field(index=True, unique=True)
    entries: list[Entry] = Relationship(back_populates="tags", link_model=EntryTagLink)
