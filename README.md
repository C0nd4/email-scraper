# email-scraper

This script will scrape a user supplied list of URLs for email addresses. The current regex should match most email addresses, but is not the complete regex for RFC 5322. The only browser currently supported is Google Chrome.

## Usage

1. Install chromedriver for your version of Google Chrome from here: https://sites.google.com/a/chromium.org/chromedriver/downloads
2. Change "CHROME_DRIVER_LOCATION" in email.scraper.py to the location of chromedriver.exe\
3. Install dependencies with `$ pip3 install -r requirements.txt`
4. Run script with `$ ./email-scraper.py -i <input_file> -o <output_file>`