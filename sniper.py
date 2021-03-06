#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from getpass import getpass
import time
import winsound
import sys
import os

scheduled_jobs = 0
browser = None

def getPassword() :
	username = input('Username\n')
	password = ''
	if sys.stdin.isatty():
		password = getpass('Password\n')
	else:
		password = input('Password...sorry it will be in the clear\n')
	return username, password

def login() :
	browser.get('https://login.frontlineeducation.com/login?signin=db554d1e950518f569b0593e54dfbaa5&productId=ABSMGMT&clientId=ABSMGMT#/login')
	WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, 'Username')))
	try :
		assert 'Frontline - Sign In' in browser.title
		elem = browser.find_element_by_name('Username')  # Find the search box
		elem.send_keys(username)
		elem = browser.find_element_by_name('Password')
		elem.send_keys(password + Keys.RETURN)
		return waitForRedirect()
	except Exception as e:
		print('error line 37')
		print(e)
		sys.stdout.flush()
		restart()
		return False

def availableJobs() :
	global scheduled_jobs
	if waitForRedirect() :
		try :
			find_full_view()
			scheduled_jobs = int(browser.find_element_by_id('ui-id-2').find_element_by_tag_name('span').text)
			elem = browser.find_element_by_css_selector('span.av').text
			if elem == '0' :
				refresh()
				return False
			else :
				checkJobs()
				return True
		except Exception as e:
			print('error line 57')
			print(e)
			sys.stdout.flush()
			restart()
			return False

def switch(job):
	schools = ['West High School', 'Tracy High School', 'Kimball High School', 'Stein Continuation High School']
	days = ['Mon', 'Tue', 'Wed', 'Thurs', 'Fri']
	durations = ['Full Day', '04:05', '6:05']
	titles = ['sdc']
	detail = job.find_element_by_css_selector('tr.detail')
	summary = job.find_element_by_css_selector('tr.summary')

	if detail.find_element_by_class_name('itemDate').text[:3] in days :
		if detail.find_element_by_class_name('durationName').text in durations :
			if detail.find_element_by_class_name('location').text in schools or summary.find_element_by_class_name('title').text[:3].lower() in titles :
				return True
			return False
		return False
	return False

def checkJobs() :
	jobs = browser.find_element_by_id('availableJobs')
	jobs = jobs.find_elements_by_css_selector('tbody.job')
	
	for job in jobs :
		if switch(job) :
			acceptJobs(job)
		else :
			acceptJobs(job) #auto accept everything

			#detail = job.find_element_by_css_selector('tr.detail')
			#school = detail.find_element_by_class_name('location').text
			#localTime = time.asctime( time.localtime(time.time()) )
			#print("Didn't like that job: " + school + " " + localTime)
			#sys.stdout.flush()
			#winsound.Beep(frequency, duration)

	refresh()
	return
def acceptJobs(job) :
	global scheduled_jobs
	summary = job.find_element_by_css_selector('tr.summary')
	# summary.find_element_by_class_name('rejectButton').click() 
	summary.find_element_by_class_name('acceptButton').click()
	acceptModal()
	detail = job.find_element_by_css_selector('tr.detail')
	school = detail.find_element_by_class_name('location').text
	localTime = time.asctime( time.localtime(time.time()) )
	time.sleep(4)
	new_job_count = int(browser.find_element_by_id('ui-id-2').find_element_by_tag_name('span').text)
	if new_job_count > scheduled_jobs :
		winsound.PlaySound('./austin_yeah.wav', winsound.SND_FILENAME)
		print('############-I accepted a job at: ' + school + "-###################" + localTime)
		scheduled_jobs = new_job_count
	else :
		winsound.PlaySound('./fail.wav', winsound.SND_FILENAME)
		print('############-I tried to get the job but I failed: ' + school + "-###################" + localTime)

	sys.stdout.flush()
	return

def acceptModal() :
	if browser.findElement(By.xpath("//div[contains(@class, 'ui-dialog ui-widget ui-widget-content ui-corner-all ui-front ui-dialog-buttons ui-draggable')]")) :
		modal = browser.findElement(By.xpath("//div[contains(@class, 'ui-dialog ui-widget ui-widget-content ui-corner-all ui-front ui-dialog-buttons ui-draggable')]"))
		button = modal.find_elements_by_tag_name('button')[1]
		button.click()

def waitForRedirect() :
	try :
		return  WebDriverWait(browser, 20).until(EC.url_to_be('https://sub.aesoponline.com/Substitute/Home'), "URL never matched")
	except Exception as e:
		print('error 121')
		print(e)
		sys.stdout.flush()
		restart()
		return False

def find_full_view() :
	try :
		WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'ui-id-2')))
	except :
		browser.find_element_by_link_text("Click Here to return to the 'Full View' of data.").click()
		try :
			WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, 'ui-id-2')))
		except :
			return Exception
		

def refresh() :
	time.sleep(1)
	browser.refresh()
	if waitForRedirect() :
		find_full_view()
		print('in refresh, after the redirect')
		sys.stdout.flush()
		availableJobs()
	return

def restart() :
	global browser
	winsound.PlaySound('./doh.wav', winsound.SND_FILENAME)
	browser.quit()
	os.system('python ' + sys.argv[0] + ' ' + sys.argv[1] + ' ' + sys.argv[2])
	sys.exit()

def startup() :
	global browser
	#browser = webdriver.Firefox() #if using firefox
	browser = webdriver.Chrome('./chromedriver.exe')
	winsound.PlaySound('./let_the_games_begin.wav', winsound.SND_FILENAME)
	if login() :
		availableJobs()

username = sys.argv[1]
password = sys.argv[2]
startup()
