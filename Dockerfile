# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9.13-alpine3.16

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install c libraries necessary for running pandas and numpy
RUN apk --no-cache add musl-dev linux-headers g++

# Install pip requirements
COPY requirements.txt .
RUN pip install --upgrade pip
RUN python -m pip install -r requirements.txt

EXPOSE 8050

WORKDIR /app
COPY . /app




# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "PDBcioos_june1.py"]
