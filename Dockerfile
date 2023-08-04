FROM python:3.9-slim as builder

# Based on https://gist.github.com/matt-bertoncello/a7296c4fc6cdbb8424ffa26b2b9b9257


# install all packages for chromedriver: https://gist.github.com/varyonic/dea40abcf3dd891d204ef235c6e8dd79
RUN apt-get update && \
    apt-get install -y xvfb gnupg wget curl unzip --no-install-recommends && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable

# copy any python requirements file into the install directory and install all python requirements.
COPY requirements.txt /requirements.txt
RUN pip install --upgrade --no-cache-dir -r /requirements.txt
RUN rm /requirements.txt # remove requirements file from container.

COPY resources /resources
COPY main.py /main.py

CMD ["python", "main.py"]



# # install all packages for chromedriver: https://gist.github.com/varyonic/dea40abcf3dd891d204ef235c6e8dd79
# RUN apt-get update && \
#     apt-get install -y xvfb gnupg wget curl unzip --no-install-recommends && \
#     wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
#     echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
#     apt-get update -y && \
#     apt-get install -y google-chrome-stable && \
#     CHROMEVER=$(google-chrome --product-version") && \
#     DRIVERVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMEVER") && \
#     wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/$DRIVERVER/chromedriver_linux64.zip" && \
#     unzip /chromedriver/chromedriver* -d /chromedriver

# # make the chromedriver executable and move it to default selenium path.
# RUN chmod +x /chromedriver/chromedriver
# RUN mv /chromedriver/chromedriver /usr/bin/chromedriver

# # copy any python requirements file into the install directory and install all python requirements.
# COPY requirements.txt /requirements.txt
# RUN pip install --upgrade --no-cache-dir -r /requirements.txt
# RUN rm /requirements.txt # remove requirements file from container.

# # copy the source code into /app and move into that directory.
# COPY src /app

# ## end builder stage.

# #####

# ## start base stage.

# # this is the image this is run.
# FROM builder

# # set the proxy addresses
# ENV HTTP_PROXY "http://134.209.29.120:8080"
# ENV HTTPS_PROXY "https://45.77.71.140:9050"

# # default entry point.
# CMD ["python", "app/webscraper.py", "-c"]
# ## end base stage.



# docker build -t kinderup_downloader .
# docker run -d --rm -v "$(pwd)"/_output:/_output kinderup_downloader
# Probar docker run -d --rm  -v "$(pwd)":/app example1
