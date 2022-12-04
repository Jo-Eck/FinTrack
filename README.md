FinTrack
(Aufgabe Montag)


###Welcome to the FinTrack ReadMe!


Quickstart with Docker:
within the project directory execute "docker-compose up". Then, in your browser, open: "localhost:8051". Good to go!

Quickstart without Docker:
Make sure you've installed Python 3.10 and PostgreSQL (and pg4, which is an install-option and a Database-frontend for PGSQL).
Create a Database with pgAdmin and load the TestDB.sql-dump using psql. Start the api with "python ./api/api.py" and then run streamlit via
"streamlit run ./frontend/app.py"


To start the application, first initialize the Database. Using pg4's PSQL app, 
execute the TestDB.sql script to prepare the DB for your transactions.