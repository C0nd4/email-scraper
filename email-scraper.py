#/usr/bin/env python3

import getopt
import re
import sys
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

CHROME_DRIVER_LOCATION = "chromedriver.exe"

def write_output(output_file, emails):
	fields = ['Email', 'Discovered On']
	output_file.writerow(fields)
	for email, site in emails:
		output_file.writerow([email, site])

def scrape_emails(urls):
	emails = set()
	email_regex = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(executable_path=CHROME_DRIVER_LOCATION, options=options)
	for url in urls:
		url = url.strip('\n')
		print('\n[*] Processing ' + url)
		try:
			driver.get(url)
			el = driver.find_element_by_tag_name('body')
			for re_match in re.finditer(email_regex, el.text):
		   		emails.add((re_match.group(), str(url)))
		   		print('[+] Email discovered: ' + re_match.group())
		except:
			print('[-] ERROR: Could not reach url ' + url)
	driver.quit()
	return emails


def main():
	input_file_name = ''
	output_file_name = ''
	urls = []
	fullCmdArguments = sys.argv
	if len(sys.argv) == 1:
		print('Invalid syntax. Use -h for help.')
		exit(1)
	argumentList = fullCmdArguments[1:]
	unixOptions = 'hi:o:'
	gnuOptions = ['help', 'input', 'output']
	try:
		arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
	except getopt.error as err:
		print (str(err))
		print('For help use the -h flag.')
		exit(1)
	for currentArgument, currentValue in arguments:
		if currentArgument in ('-h', '--help'):
			print('\nUsage: ./email-scraper.py -i <input_file> -o <output_file>')
			print('\nOPTIONS:')
			print('  -i: Input file. Specify a text list of domains to query.')
			print('  -o: Output file. Will output data into a specified CSV file.')
			exit(0)
		elif currentArgument in ('-i', '--input'):
			input_file_name = currentValue
		elif currentArgument in ('-o', '--output'):
			output_file_name = currentValue

	if not input_file_name or not output_file_name:
		print('Invalid syntax. Use -h for help.')
		exit(1)

	try:
		input_file = open(input_file_name, 'r')
		for line in input_file:
			urls.append(line)
		input_file.close()
	except:
		print('Could not open input file')
		exit(1)
	try:
		output_csv = open(output_file_name, 'w', newline='')
		output_file = csv.writer(output_csv)
	except:
		print('Could not open output file')
		exit(1)

	write_output(output_file, scrape_emails(urls))
	output_csv.close()
	print('\n[*] COMPLETED')
	exit(0)

if __name__ == '__main__':
	main()