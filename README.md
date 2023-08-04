# KinderUp Picture Downloader
Download all pictures and videos from KinderUp app. Written in Python.

## How does it works
It can be executed using Docker or locally.

### Algorithm:
Using Selenium the program will:
1. Open a Chrome Browser
2. Navigate to the application login view (It can be configured in the resources/config.json file)
3. Navigate to the Pictures view
4. Scroll down until all multimedia content is loaded
5. Start dowloading all pictures, from older to newer
6. Download all videos, from older to newer

All multimedia files are stored inside the a folder in the _output directory.
It can take around 20-30 minutes to download ~ 1300 multimedia elements.
 
## Execution:
### Docker
#### Build
From the root: 

	$ docker build -t kinderup_downloader .

#### Run
From the root:

	docker run -d --rm -e KINDERUP_USER=<your_username> -e KINDERUP_PASS=<your_password> -v "$(pwd)"/_output:/_output:Z kinderup_downloader

### Locally
Follow the steps:
1. Have Chrome and python 3 installed
2. Install Python dependencies ([Virtualenvs](https://docs.python.org/3/library/venv.html) are highly recommended)

		$ pip install -r requirements.txt
3. Execute
		
		$ python main.py
