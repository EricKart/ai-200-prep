FROM mcr.microsoft.com/azurelinux/base/python:3.12
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY server.py .
EXPOSE 11434
CMD ["python3", "server.py"]
