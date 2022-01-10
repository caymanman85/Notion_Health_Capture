import settings
import utils
import time
import datetime
import json

# refresh access token if it has expired.
if utils.exchange_code(settings.code) != '200':
    utils.Token_Refresh()
else:
    print('Access Token Obtained')

# Refresh all data sources

# Check status file for the status of all sources. If the source status is not "Completed", then continue to re-run sync status
# Until all 3 sources (Activity, Sleep, and Weight are refreshed)

for source in settings.DATA_SOURCES:
    utils.Fitness_Source_Refresh(source)
    print('Refreshing: ', source)
    print('--------------------')

    # Try up to 20 times monitoring the status of the sync request.
    for _ in range(settings.RETRIES):
        APIStatus = utils.Synchronization_Status()

        if APIStatus == 'Complete':
            break

        time.sleep(5)
        utils.Synchronization_Status()

utils.sleep_capture()
utils.weight_capture()
utils.activity_capture()

# Read the refresh date to determine if the most update to date data is available.
with open('Health\weight.json') as f:
        data = json.load(f)
        refresh_date = data['date']

        today = datetime.datetime.now().strftime('%d-%B-%Y')
        refresh_date = str(datetime.datetime.fromtimestamp(float(refresh_date) / 1000, tz=datetime.timezone.utc).strftime('%d-%B-%Y'))

if refresh_date == today:
    print('Update Starting')
    print('-------------------')

    if utils.notion_sleep_check() == "":
        utils.notion_sleep_update()
    else:
        print("Sleep Data already updated")
        print('-------------------')
    
    utils.notion_weight_update()
    utils.weight_Fitness()
    utils.bmi_Fitness()
    utils.body_fat_Fitness()

    print('Notion Updated')

else:
    print("Huawei Data not updated yet in Fitness Syncer")
