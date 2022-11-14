FROM python:3.9
WORKDIR /app
COPY requirements_frontend.txt ./requirements
RUN pip3 install -r requirements
COPY . /app

EXPOSE 8501
ENV API_HOST=172.17.0.2
ENV API_PORT=8888

ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]