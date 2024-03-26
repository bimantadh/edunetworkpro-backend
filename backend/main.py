from routers import applications, consultancy,file,university,users,auth,students,notes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.include_router(applications.router)
app.include_router(consultancy.router)
app.include_router(file.router)
app.include_router(university.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(students.router)
app.include_router(notes.router)


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://192.168.1.81:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
