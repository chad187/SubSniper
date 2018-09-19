from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import winsound

frequency = 2500  # Set Frequency To 2500 Hertz
duration = 3000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)

Username = '2096240502'
Password = '7908'

def login(browser) :
	browser.get('https://login.frontlineeducation.com/login?signin=db9ca07520392d5d8f625c973b80174c&productId=ABSMGMT&clientId=ABSMGMT#/login')

	try :
		assert 'Frontline - Sign In' in browser.title

		elem = browser.find_element_by_name('Username')  # Find the search box
		elem.send_keys(Username)

		elem = browser.find_element_by_name('Password')
		elem.send_keys(Password + Keys.RETURN)
		return waitForRedirect(browser)
	except :
		return False

def availableJobs(browser) :
	time.sleep(5)
	waitForRedirect(browser)
	print('in availableJobs after redirect')
	try :
		elem = browser.find_element_by_css_selector('span.av').text
		if elem == '0' :
			refresh(browser)
			return False
		else :
			checkJobs(browser)
			return True
	except :
		browser.quit()
		time.sleep(4)
		startup()
		return False

def switch(job):
	schools = ['Granada High School', 'Livermore High School', 'Del Valle Continuation High School']
	days = ['Wed', 'Thu', 'Fri']
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

def checkJobs(browser) :
	jobs = browser.find_element_by_id('availableJobs')
	jobs = jobs.find_elements_by_css_selector('tbody.job')
	
	for job in jobs :
		if switch(job) :
			acceptJobs(browser, job)
		else :
			detail = job.find_element_by_css_selector('tr.detail')
			school = detail.find_element_by_class_name('location').text
			localTime = time.asctime( time.localtime(time.time()) )
			print("Didn't like that job: " + school + " " + localTime)

	refresh(browser)
	return
def acceptJobs(browser, job) :
	summary = job.find_element_by_css_selector('tr.summary')
	# summary.find_element_by_class_name('rejectButton').click() 
	summary.find_element_by_class_name('acceptButton').click()
	detail = job.find_element_by_css_selector('tr.detail')
	school = detail.find_element_by_class_name('location').text
	localTime = time.asctime( time.localtime(time.time()) )
	print('############-I accepted a job at: ' + school + "-###################" + localTime)
	winsound.Beep(frequency, duration)
	return

def waitForRedirect(browser) :
	try :
		return  WebDriverWait(browser, 20).until(EC.url_to_be('https://sub.aesoponline.com/Substitute/Home'), "URL never matched")
	except :
		return False

def refresh(browser) :
	time.sleep(61)
	browser.refresh()
	waitForRedirect(browser)
	print('in refresh, after the redirect')
	availableJobs(browser)
	return

def startup() :
	browser = webdriver.Firefox()
	if login(browser) :
		availableJobs(browser)
	else :
		browser.quit()
		time.sleep(4)
		startup()

startup()