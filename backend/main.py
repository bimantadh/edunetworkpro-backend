from routers import applications, consultancy,file,university,users

from fastapi import FastAPI

app = FastAPI()


app.include_router(applications.router)
app.include_router(consultancy.router)
app.include_router(file.router)
app.include_router(university.router)
app.include_router(users.router)