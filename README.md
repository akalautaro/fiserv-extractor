# Fiserv scraper

Script made to scrape and download txt files from <a href="www.fiserv.com.ar">Fiserv</a>

## Disclaimer (?)

_This script was made to solve a personal problem at work and to automate a repetitive task (downloading ~35 files manually, every month)._

_While I've tried to follow Python best practices, there may be bugs, typos, or things that could simply be improved (see end of readme)._ 

_I am not responsible for the use that is given to the script._

## <h2>Steps to follow on the web</h2>
1. Go to [Fiserv](https://www.fiserv.com.ar/) and login
2. Go to tab <b>"Movimientos"</b>, then <b>"Liquidación electrónica"</b>
3. Scraping filenames to know which ones to download (div//div//table//tbody//tr[<b>n</b>]//td[1]//b)
4. Click button (div//div//table//tbody//tr[<b>n</b>]//td[5]//b) to dowload file
5. Process the files with script [procesar_liquidacion.py](src/liquidacion/procesar_liquidacion.py) (private script 🤪)

## <h2>Pre-configurations</h2>

First, we need to install all the necessary packages and libs on our system or in a virtual environment. In a terminal inside the project dir:

`pip install -r requirements.txt`

Config our credentials on a `config.ini` file, located on root project dir. You have an [example](config_example.ini) here to look the file structure.

Note: the logger can be configured as desired on [base_logger.py](src/base_logger.py) file

## <h2>Run the script</h2>

To run the script, launch a terminal on the project directory and execute:

`python src/extractor.py`

_<h3>Crontab example:</h3>_

To modify our crontab file on Linux, launch a terminal and run `crontab -e`. Then add the following line:

`0 12 * * * /path/to/code/script.py >> /path/to/some/log.txt 2>&1`

_This way the script would run every day at 12 o'clock, saving errors to a file called log.txt_

Note: to make the script work with cron we need to add chromedriver to our path, add shebang and change the permissions of the .py file (sudo chmod a+x script.py), and maybe some other Linux "tricks" depending of our system 🥴

## <h2><b>Things to improve</b></h2>

In order of importance:

- _Improve performance and speed avoiding unnecessary `sleeps` and `for cicles`_
- _Improve validations on `try-except` blocks_
- _Implement and improve [`check_if_exists`](src/extractor.py), [`check_local_files`](src/extractor.py) and [`delete_unnecessary_files`](src/extractor.py)_
- _Add commands (maybe with `python-click`) to choose number of files to download (adding pagination to the scraper) and also to set the log-level_
- _Implement some tool to run the script avoiding using crontab_
- _Add AirFlow to automate the processing_

Obviously, feel free to fork the code and make a pull request 😊

<hr>
<small>Made with ❤ and 🐍 by <a href="https://twitter.com/akalautaro">akalautaro</a>.</small>
