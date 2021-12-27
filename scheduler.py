#CURRENTLY IN BETA MODE
#USE THIS WITH CAUTION AS CODE HAS NOT BEEN THOROUGHLY TESTED OUT WITH 2FA
from datetime import datetime, time
import time
from setup import run_everything
from send_email import filter_monitor

#2FA is default enabled across the program
two_FA_enabled=True

#also send an Apple Watch suitable QR code
to_watch=True

run_everything(two_FA_enabled=two_FA_enabled, to_watch=to_watch)
while True:
    if(two_FA_enabled):
        if filter_monitor(query="[RUN AUTO TROY]"):
            run_everything(to_watch=to_watch)
        else:
            time.sleep(60)
    else:
        ending = datetime.now().time()
        hour, minute = [int(each) for each in ending.strftime("%H:%M").split(":")]
    
        if(hour==0 and minute==22):
            run_everything(two_FA_enabled=False, to_watch=to_watch)
            time.sleep(65)
