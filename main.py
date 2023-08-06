from fastapi import FastAPI
from api import users, sections, courses


app = FastAPI(
    title="Fast API LMS",
    description="LMS for managing students and courses.",
    version="0.0.1",
    contact={
        "name": "Nick",
        "email": "dynin.nikolaj2010@yandex.ru"
    },
    license_info={
        "name": "Proston_Tech"
    }
)

app.include_router(users.router)
app.include_router(sections.router)
app.include_router(courses.router)


