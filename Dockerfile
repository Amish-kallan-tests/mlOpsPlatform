FROM python:3.10-slim
# RUN apt-get update && apt-get install -y curl && \
#     curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
#     apt-get install -y nodejs && \
#     npm install -g nodemon
# WORKDIR /app
# ENV FLASK_APP=app.py
# ENV FLASK_ENV=development
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# EXPOSE 8001
EXPOSE 5000
CMD ["python3", "app.py"]
