FROM python:3.9
WORKDIR /app
COPY requirements_api.txt ./requirements
RUN pip3 install -r requirements
COPY . /app

#ENV API_HOST=fintrack_api
#ENV API_PORT=8888
#ENV API_DEBUG=True
#ENV DB_HOST=fintrack_db
#ENV DB_NAME=FinTrack
#ENV DB_USER=postgres
#ENV DB_PASSWORD=myPassword
#ENV FLASK_APP=api.py
EXPOSE 8888
ENTRYPOINT [""]
CMD ["python", "api.py"]
