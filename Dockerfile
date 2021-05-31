FROM python:3.8-slim
ADD src /deploy/src
COPY ./requirements.txt /deploy/
WORKDIR /deploy/
RUN pip install -r requirements.txt
EXPOSE 80
ENTRYPOINT ["python", "src/app.py"]
