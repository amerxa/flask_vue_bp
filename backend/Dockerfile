FROM python

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app 

# install dependencies
RUN apt-get update && apt-get install -y netcat
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# copy files
COPY webapp/* .

# run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]