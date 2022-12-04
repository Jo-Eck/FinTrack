FinTrack

## Welcome to the FinTrack ReadMe!
This project is a simple web-application for tracking your personal finances. It is a work in progress and is not yet ready for production. <br>
It was created as as part of joined university project for the course "Implementations" at the Cooperative State University Baden-Württemberg (DHBW). <br> 
<br>
The project is written in Python and uses the Streamlit framework for the frontend and Flask for the backend. The Database is a PostgreSQL-DB.


### Quickstart with Docker:
This project is intended to be run via  Docker.
To start the application, make sure you have Docker installed on your machine. <br>
To install Docker, follow the instructions on the official Docker website: https://docs.docker.com/get-docker/

Once Docker is installed, clone the repository and execute `docker-compose up` in the project directory.
This will start the application and the database. <br>
The application will be available at http://localhost:8501



### Quickstart without Docker:
Alternatively, you can run the application without Docker, which is useful for development purposes, but not necessarily recommended.

Make sure you've installed Python 3.10 and PostgreSQL (and pg4, which is an install-option and a Database-frontend for PGSQL).<br>
To install Python, follow the instructions on the official Python website: https://www.python.org/downloads/
To install PostgreSQL, follow the instructions on the official PostgreSQL website: https://www.postgresql.org/download/
To install pg4, follow the instructions on the official pg4 website: https://www.pgadmin.org/download/

Before you can run the application, you need to create a database and a user for the application.
To do so, run the following commands in the PostgreSQL shell:

    CREATE DATABASE FinTrack;

and load the database dump from the project directory:

    sudo -u postgres psql FinTrack < ./database/DataBase.sql

To start the application, run the following commands in the project directory:

    pip install -r requirements.txt
    python ./api/api.py
    streamlit run ./frontend/app.py

The application will then be available at http://localhost:8501

------------------------------------------------------------------------------------------------------------------------------
This project is the result of a joint project by the following students:
- Jan Roederer
- Jon Eckerth
- Kilian Seelbach

This code can also be found on GitHub: https://github.com/Jo-Eck/FinTrack 
