import hashing
from get_env import hold_creds
import web_scraper
from send_email import send_error_message

def run_everything(two_FA_enabled=True, to_watch=True):
    if hold_creds()[0] and hold_creds()[1]:
        try:
            web_scraper.auto_troy(two_FA_enabled=True, to_watch=True)
        except Exception as e:
            error_received = str(e)
            default_email_address = '{}@usc.edu'.format(hold_creds[0])
            message_body = 'Auto Troy has encountered an error! Program cannot proceed further until it is restarted due to a {} error. If restarting does not fix this issue, please review code for any bugs/mistakes. Otherwise, please create an issue on the Github repo'.format(e)
            send_error_message(default_email_address, message_body)         
    else:
        hashing.command_line_encode_details()
        web_scraper.auto_troy(two_FA_enabled=True, to_watch=True)
        
#uncomment this to setup credentials
#run_everything()

