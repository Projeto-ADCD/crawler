## Instructions to install all the necessary code

- This project utilizes anaconda. You can install here: https://anaconda.org/
- After installation run the follow commands:
```
$ conda create --name projeto1-crawler
$ conda activate projeto1-crawler
$ pip install selenium
$ wget https://chromedriver.storage.googleapis.com/102.0.5005.61/chromedriver_linux64.zip 
$ zip chromedriver_linux64.zip
$ sudo mv chromedriver /usr/bin
$ pip install -r requirements.txt
```
- The project should run now.