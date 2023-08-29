FROM python:3.11

LABEL maintainer="Priyanka B"

ENV DOCKER=true


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update
RUN pip install fastapi uvicorn
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Build docker
# docker build -t app .
# docker-compose rm -fs
















# FROM python:3.7-slim

# LABEL maintainer="Shamil Kayanolil"

# ENV DOCKER=true
# COPY pyproject.toml .

# # RUN pip install --no-cache-dir --upgrade pip && \
# #     pip install --no-cache-dir poetry && \
# #     poetry install

# # RUN apt-get update
# COPY requirements.txt .
# # RUN pip install --no-cache-dir uvicorn==0.18.2
# RUN pip install --no-cache-dir -r requirements.txt
# RUN apt-get update
# COPY . .
# EXPOSE 8000
# # RUN ls -l
# # CMD ["poetry", "run", "hypercorn", "/app/main:app", "--bind", "0.0.0.0:8000", "--reload"]
# # CMD ["poetry", "run", "hypercorn", "app/main:app", "--bind", "0.0.0.0:8000", "--reload"]
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]