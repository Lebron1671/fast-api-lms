# Fast API LMS

## Table of Contents

1. [Overview & Requirements](#overview-&-requirements)
1. [Running Locally](#running-the-app-locally)
1. [Tech Stack](#tech-stack)
1. [Schema](#schema)

## Overview & Requirements

This is a learning management system where teachers can manage student and students can see their courses.

You can perform the next operations:

- CRUD operations on users and courses
- Assign course to teacher and students
- Teacher and students can see their courses

## Running the App Locally

1. Make sure Python, Poetry, and Postgres are installed. Postgres must be running. *I run PostgreSQL in Docker*
2. Create a virtual environment: `python -m venv venv`
3. Install packages: `poetry install`
4. Run the development server: `uvicorn main:app --reload`

## Tech Stack

- Fast API
- Python
- Poetry
- Postgres
- SQL Alchemy
- Alembic
- Pydantic

## Schema

**User**

- id: pk
- email: str
- first_name: str
- last_name: str
- role: enum (student, teacher)
- birthday: date
- phone: str
- is_active: bool


**Course**

- id: pk
- teacher_id: fk
- title: str
- description: str (TextField)
- academic_hours: int
- classroom: str


**StudentCourse**

*This model is used for assigning courses to students.*

- student_id
- course_id
