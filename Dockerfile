FROM python:3.9-slim as builder

# install all packages for chromedriver: https://gist.github.com/varyonic/dea40abcf3dd891d204ef235c6e8dd79
RUN apt-get update && \
    apt-get install -y xvfb gnupg wget curl unzip --no-install-recommends && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable

# copy any python requirements file into the install directory and install all python requirements.
COPY app/requirements.txt /requirements.txt
RUN pip install --upgrade --no-cache-dir -r /requirements.txt
RUN rm /requirements.txt # remove requirements file from container.

COPY app /app

WORKDIR /app

CMD ["python", "main.py"]


# Build example:
# docker build -t kinderup_downloader .

# Run example:
# $ docker run --rm -e KINDERUP_USER=<user_name> -e KINDERUP_PASS=<password> -v "$(pwd)"/app:/app:Z kinderup_downloader

# Run Interactive
# docker run -it  -e KINDERUP_USER=<user_name> -e KINDERUP_PASS=<password> -v "$(pwd)"/app:/app:Z kinderup_downloader bash
