# KinderUp Picture Downloader
Download all pictures and videos from KinderUp app. Written in Python.

## How does it works
It can be executed using Docker or locally.

### Algorithm:
Using Selenium the program will:
1. Open a Chrome Browser
2. Navigate to the application login view (It can be configured in the resources/config.json file)
3. Navigate to the Pictures view
4. Scroll down until all multimedia content is loaded. At this point, all request related with multimedia content are saved.
5. Start downloading all pictures and videos, from older to newer, using the saved requests.

All multimedia files are stored inside the a folder in the '_output' directory.
It can take around 40-60 minutes to download ~ 1300 multimedia elements.
 
## Execution:
### Docker
#### Build
From the root: 

	$ docker build -t kinderup_downloader .

#### Run
From the root:

	docker run -d --rm -e KINDERUP_USER=<your_username> -e KINDERUP_PASS=<your_password> -v "$(pwd)"/app:/app:Z kinderup_downloader

### Locally
Follow the steps:
1. Have Chrome and python 3 installed
2. Install Python dependencies ([Virtualenvs](https://docs.python.org/3/library/venv.html) are highly recommended)

		$ pip install -r requirements.txt
3. Execute
		
		$ python main.py