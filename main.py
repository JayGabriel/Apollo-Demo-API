from __future__ import annotations
import os
import strawberry
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from strawberry.fastapi import GraphQLRouter

@strawberry.type
class User:
    id: strawberry.ID
    name: str
    age: int
    friends: list["User"]
    motto: str
    image_url: str

    @strawberry.field
    def process_title(self) -> str:
        return f"Hello, my name is: {self.name}. I am {self.age} years old. I have {len(self.friends)} friends."

# Mock data
mock_users = [
    User(
        id="0",
        name="John Doe",
        age=30,
        friends=[],
        motto="Live and let live.",
        image_url="https://randomuser.me/api/portraits/men/0.jpg"
    ),
    User(
        id="1",
        name="Jane Smith",
        age=28,
        friends=[],
        motto="Carpe diem.",
        image_url="https://randomuser.me/api/portraits/women/1.jpg"
    ),
    User(
        id="2",
        name="Kevin Nguyen",
        age=32,
        friends=[],
        motto="Stay curious.",
        image_url="https://randomuser.me/api/portraits/men/2.jpg"
    ),
    User(
        id="3",
        name="Jack Doe",
        age=25,
        friends=[],
        motto="Never give up.",
        image_url="https://randomuser.me/api/portraits/men/3.jpg"
    ),
    User(
        id="4",
        name="Janice Doe",
        age=27,
        friends=[],
        motto="Dream big.",
        image_url="https://randomuser.me/api/portraits/women/4.jpg"
    ),
    User(
        id="5",
        name="Shaniqua Doe",
        age=29,
        friends=[],
        motto="Be yourself.",
        image_url="https://randomuser.me/api/portraits/women/5.jpg"
    )
]

# Assign friends (using references from mock_users)
mock_users[0].friends = [mock_users[1], mock_users[2]]  # John Doe's friends: Jane, Kevin
mock_users[1].friends = [mock_users[0], mock_users[2]]  # Jane's friends: John, Kevin
mock_users[2].friends = [mock_users[0], mock_users[1]]  # Kevin's friends: John, Jane
mock_users[3].friends = [mock_users[4], mock_users[5]]  # Jack's friends: Janice, Shaniqua
mock_users[4].friends = [mock_users[3], mock_users[5]]  # Janice's friends: Jack, Shaniqua
mock_users[5].friends = [mock_users[3], mock_users[4]]  # Shaniqua's friends: Jack, Janice

# QUERIES
@strawberry.type
class Query:

    @strawberry.field
    def test_method(self) -> str:
        return "What's up iOS!!!"
    
    @strawberry.field
    def hello(self, name: str) -> str:
        return f"Hello {name}"
    
    @strawberry.field
    def getDefaultUser(self) -> User:
        return mock_users[0]
    
    
# Assemble schema
schema = strawberry.Schema(query=Query)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten for prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
graphql_app = GraphQLRouter(schema, graphiql=True)
app.include_router(graphql_app, prefix="/graphql")

# Export schema to schema.graphql
with open("schema.graphqls", "w") as f:
    f.write(schema.as_str())

@app.get("/")
def healthcheck():
    return {"status": "ok", "graphql": "/graphql"}

@app.get("/schema.graphqls")
def get_schema():
    return FileResponse("schema.graphqls", media_type="text/plain")

# ...existing code...

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port)