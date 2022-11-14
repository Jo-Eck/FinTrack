FROM python:3.9
WORKDIR /app
COPY requirements_api.txt ./requirements
RUN pip3 install -r requirements
COPY . /app

EXPOSE 8888

ENV API_HOST=172.17.0.2
ENV API_PORT=8888
ENV API_DEBUG=True
ENV DB_HOST=0.0.0.0
ENV DB_NAME=FinTrack
ENV DB_USER=postgres
ENV DB_PASSWORD=myPassword
ENV FLASK_APP=api.py

ENTRYPOINT [""]
CMD ["python", "api.py"]
