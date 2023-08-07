from fastapi import FastAPI
from api import users, sections, courses
from db.db_setup import engine

from db.models import user, course

#user.Base.metadata.create_all(bind=engine)
#ourse.Base.metadata.create_all(bind=engine)


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


