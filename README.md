# Auto Troy
Auto Troy automates the USC TrojanCheck for a compliant student. What started out as a distraction activity to do at Starbucks at 6:30am after a sleepless night turned into a built out project. View this Medium article(in progress) to see how this whole thing works.

## Forewarning!!!
Using the code means that you are compliant with USC's Covid policies and you do not have COVID-19. I published this repo in hopes that other compliant people will benefit from this and will enable them to be one step closer to a day without worrying about Covid and Covid protocols. 

## Get Google Gmail API Credentials
The credentials.json file must be generated from the https://console.cloud.google.com/. Search for the Gmail API and enable it. Then go to Credentials and created an OAuth 2.0 Client IDs credential. Download the file and rename to credentials.json and move it into the project folder. When send_day_pass() is run, the credential process will automatically run to get the necessary token values to be able to send an email.

## 1. Setting up folders
The ./phone_screenshots and ./watch_screenshots folders have dummy .txt files called placeholder. They need to be deleted before running the code. They were created so these folders existed in the repository.
## 2. Download packages and setup credentials
There are a few dependent python packages to download before running this program (can be found in requirements.txt)
```python
python -m pip install -r requirements.txt
```
Setup.py handles all of the setup code from obtaining the login credentials to running the webscraper. If credentials are not found, you will be prompted to enter them in the command line. If they are found, the automation software will run.
```python
#uncomment this function to handle all setup processes as well as hash the credentials
#will be prompted in command line to input USC credentials
run_everything()
``` 
## 3. Running program
* Manually run Auto Troy:
```python
 python web_scraper.py
```
* Schedule when to run Auto Troy:
```python
 python schedule_date.py
```
  _Default scheduled to run at 12:59am and needs to be running at scheduled time to work_

To change when the program runs, look at line 10 in schedule_date.py (shown below) and write in your preferred time (24 hour period).
```python
 if(hour==0 and minute==59):
     run_everything()
     time.sleep(65)
```
## Sending emails
send_email.py handles commands to send an email. The send_day_pass() is run by web_scraper.py once the screenshot(s) have been recorded: 
```python
def send_day_pass(filepaths, email_address, to_watch):
    phone_filepath, watch_filepath = filepaths
    get_service = get_creds()
    phone_develop_message = create_message_with_attachment(email_address, email_address, '[PHONE] TROJANCHECK QR SCREENSHOT', 'Screenshot of QR Code taken by Automate TrojanCheck. Person has complied with USC policies and is using this program to obtain QR code.\n', phone_filepath)
    watch_develop_message = create_message_with_attachment(email_address, email_address, '[WATCH] TROJANCHECK QR SCREENSHOT', 'Screenshot of QR Code taken by Automate TrojanCheck. Person has complied with USC policies and is using this program to obtain QR code.\n', watch_filepath)
    phone_get_out_of_here = send_message(get_service, user_id='me', message=phone_develop_message)
    if to_watch:
      watch_get_out_of_here = send_message(get_service, user_id='me', message=watch_develop_message)
```
To change the email address, change second argument of send_day_pass() on line 142 and line 12 on setup.py to your preferred email. By default, it uses the @usc.edu email address. Additionally, if you do not have an Apple Watch/don't need solely the QR code, set to_watch to False. 

## Handling of login credentials 
The login credentials are hashed before they are stored. While the credentials are only stored locally, hashing it provides an added security layer. Furthermore, adding in the credentials to the environmental variables is a good idea. **This does not mean that this program or author is responsible if this information is leaked!** 

## Things in process
* Timeout Error: Currently, if webdriver is unable to open Chrome, the program falls into an infinite loop. This problem is being investigated further (debugging to see if the error is capturable in order to force a reboot of webdriver. 

* Two Factor Authentication (2FA) support: This program assumes that after logging in, the questionaire page comes up. There is a solution that allows for the program to click on the 2FA buttons but would require the user to be able to accept login (especially an issue if program is set up to run in the middle of the night). 2FA provider does have Python API support.
