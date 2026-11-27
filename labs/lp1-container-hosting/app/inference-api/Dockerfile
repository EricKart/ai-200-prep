FROM mcr.microsoft.com/azurelinux/base/python:3.12
ARG APP_VERSION=v1
ENV APP_VERSION=$APP_VERSION PYTHONUNBUFFERED=1
WORKDIR /app
COPY app.py .
EXPOSE 5000
CMD ["python3", "app.py"]
