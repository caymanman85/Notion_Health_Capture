import settings
import json
import requests
import datetime

def exchange_code(code):

    with open('Health\data\data.json') as f:
        data = json.load(f)
        code = data['access_token']
    
    data = {
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code':code,
        'redirect_uri': settings.REDIRECT_URI,
    }

    r = requests.request('POST',settings.API_ENDPOINT,data=data,headers=settings.data_headers) 
    
    data = r.json()
    
    if r.status_code != 200:
        print('Could Not Exchange Authorisation Token')
    
    else:
        with open('Health\data.json', 'w') as f:
            json.dump(data, f)
    
    return r.status_code

def Token_Refresh():
    print('Refreshing Token')

    with open('Health\data\data.json') as f:
        data = json.load(f)
        refresh_token = data['refresh_token']

    refresh_headers = {
    "grant_type": 'refresh_token',
    "refresh_token": refresh_token,
    "client_id": settings.CLIENT_ID,
    "client_secret": settings.CLIENT_SECRET,
    "redirect_uri": settings.REDIRECT_URI
    }

    content_headers = {
        'content-type': 'application/x-www-form-urlencoded'
    }

    data_source_id = 'https://api.fitnesssyncer.com/api/oauth/access_token'
    
    pg_readurl = data_source_id
    
    res = requests.request("POST",pg_readurl, params = refresh_headers,headers = content_headers)

    data = res.json()

    if res.status_code != 200:
        print('Error Refreshing Token')
    else:
        with open('Health\data\data.json', 'w') as f:
            json.dump(data, f, indent= 4)
        
        print('Access_Token refreshed')

def Fitness_Source_Refresh(source):
    
    with open('Health\data\data.json', 'r') as f:
        data = json.load(f)
        access_token = data['access_token']

    activity_data_headers = {
    'content-type': 'application/x-www-form-urlencoded',
    "Authorization": "Bearer " + access_token
    }

    API_REFRESH_ENDPOINT = f'https://api.fitnesssyncer.com/api/providers/sources/{source}/refresh'

    res = requests.request("POST",API_REFRESH_ENDPOINT, headers = activity_data_headers)
    
    refresh = res.json() 
    print(res.status_code)
    print('-----------------------------')
    
def Synchronization_Status():

    with open('Health\data\data.json') as f:
        data = json.load(f)
        access_token = data['access_token']

    activity_data_headers = {
    'content-type': 'application/x-www-form-urlencoded',
    "Authorization": "Bearer " + access_token
    }

    res = requests.request("GET",settings.API_SYNC_ENDPOINT, headers = activity_data_headers)
    
    now = datetime.datetime.now()

    with open('Health\data\status.json', 'w') as f:
            refresh = res.json()
            json.dump(refresh, f, indent = 4)
            print(now,': Status: ',refresh['results'][0]['status'])

    return refresh['results'][0]['status']

def capture_notion_database_ID():

    db_readurl = f'https://api.notion.com/v1/databases/{settings.notion_databaseID}/query'
    res = requests.request("POST",db_readurl, headers = settings.db_headers)
    data = res.json()

    return data['results'][0]['id'] 

def notion_sleep_check():

    notion_PageID = capture_notion_database_ID()

    pg_readurl = f'https://api.notion.com/v1/pages/{notion_PageID}'

    #Return the current results of the Sleep Data.  If Popoulated stop, if not, populate:
    res = requests.request("GET",pg_readurl, headers = settings.headers)

    data = res.json()

    return data['properties']['Sleep Start Time (Calculated)']['formula']['number']

def sleep_capture():

    with open('Health\data\data.json') as f:
        data = json.load(f)
        access_token = data['access_token']
    
    activity_data_headers = {
    'content-type': 'application/x-www-form-urlencoded',
    "Authorization": "Bearer " + access_token
    }

    res = requests.request("GET",settings.sleep_data_source_id, headers = activity_data_headers)
    
    sleep_data = res.json() 

    with open('Health\data\sleep.json', 'w') as f:
            json.dump(sleep_data, f, indent= 4) 

    #convert Data, Awake time, and bed time from milliseconds to normal time
    awake_time_in_millis = json.dumps(sleep_data['items'][0]['awakeTime'])
    bed_time_in_millis = json.dumps(sleep_data['items'][0]['bedTime'])
    
    Awake_Time_Hour = str(datetime.datetime.fromtimestamp(float(awake_time_in_millis) / 1000, tz=datetime.timezone.utc).strftime('%H'))
    Bed_Time_Hour = str(datetime.datetime.fromtimestamp(float(bed_time_in_millis) / 1000, tz=datetime.timezone.utc).strftime('%H'))
    Awake_Time_Mins = str(datetime.datetime.fromtimestamp(float(awake_time_in_millis) / 1000, tz=datetime.timezone.utc).strftime('%M'))
    Bed_Time_Mins = str(datetime.datetime.fromtimestamp(float(bed_time_in_millis) / 1000, tz=datetime.timezone.utc).strftime('%M'))
    Sleep_Efficiency = json.dumps(sleep_data['items'][0]['efficiency'])

    return [Awake_Time_Hour, Awake_Time_Mins,Bed_Time_Hour,Bed_Time_Mins,Sleep_Efficiency]

def weight_capture():

    with open('Health\data\data.json') as f:
        data = json.load(f)
        access_token = data['access_token']
    
    activity_data_headers = {
    'content-type': 'application/x-www-form-urlencoded',
    "Authorization": "Bearer " + access_token
    }

    res = requests.request("GET",settings.weight_data_source_id, headers = activity_data_headers)
    weight_data = res.json()

    with open('Health\data\weight.json', 'w') as f:
            json.dump(weight_data['items'][0], f, indent= 4)

    bmi = json.dumps(weight_data['items'][0]['bmi']) 
    fatRatio = json.dumps(weight_data['items'][0]['fatRatio'])
    weight = json.dumps(weight_data['items'][0]['weight'])
    muscleMass = json.dumps(weight_data['items'][0]['muscleMass'])

    # print(json.dumps(weight_data['items'][0], indent=4,sort_keys=True)) 

    return([bmi, fatRatio, weight,muscleMass])

def activity_capture():
    with open('Health\data\data.json') as f:
        data = json.load(f)
        access_token = data['access_token']
    
    activity_data_headers = {
    'content-type': 'application/x-www-form-urlencoded',
    "Authorization": "Bearer " + access_token
    }

    res = requests.request("GET",settings.activity_data_source_id, headers = activity_data_headers)
    activity_data = res.json()

    with open('Health\data\_activity.json', 'w') as f:
            json.dump(activity_data['items'], f, indent= 4)  

def notion_weight_update():
    #connect to notion and update daily tracking data points for the latest day.
    list = weight_capture()

    notion_PageID = capture_notion_database_ID()

    pg_readurl = f'https://api.notion.com/v1/pages/{notion_PageID}'

    notion_databaseID = 'b32c01ae05114af282f309bf4337ac0c'

    res = requests.request("PATCH",pg_readurl, headers = settings.headers,
                          json={
        "parent": {"database_id": notion_databaseID},
        "properties": {
            'BMI': {'number': round(float(list[0]),2)},
            'Body Fat Rate': {'number': round(float(list[1]),2)/100}, 
            'Lbs.': {'number': round(float(list[2]),2)},
            'Muscle Mass': {'number': round(float(list[3]),2)}, 
            },
        },
    )
    print('Weight Tracking Update: ',res.status_code)

    #connect to notion and update value outcome goal 1 for weight.
    pg_readurl = f'https://api.notion.com/v1/pages/{settings.WEIGHT_GOAL_BLOCK_ID}'

    res = requests.request("PATCH",pg_readurl, headers = settings.headers,
                          json={
        "properties": { 
            'Goal': {'number': round(float(list[2]),2)},
            },
        },
    )

    #connect to notion and update value outcome goal 2 for weight.
    pg_readurl = f'https://api.notion.com/v1/pages/{settings.WEIGHT_GOAL_BLOCK_ID_2}'

    res = requests.request("PATCH",pg_readurl, headers = settings.headers,
                          json={
        "properties": { 
            'Goal': {'number': round(float(list[2]),2)},
            },
        },
    )

    print('Weight Goal Update: ', res.status_code)

    #connect to notion and update value outcome goal for bmi.
    pg_readurl = f'https://api.notion.com/v1/pages/{settings.BMI_GOAL_BLOCK_ID}'

    res = requests.request("PATCH",pg_readurl, headers = settings.headers,
                          json={
        "properties": { 
            'Goal': {'number': round(float(list[0]),2)},
            },
        },
    )
    print('BMI Goal Update: ',res.status_code)

def weight_Fitness():
    
    list = weight_capture()
    
    #connect to the Health pillar and update the weight block.

    pg_readurl = f'https://api.notion.com/v1/blocks/{settings.weight_block_ID}'

    res = requests.request("PATCH",pg_readurl, headers = settings.headers,
                          json={
        "heading_1": {
        "text": [
            {
                "plain_text": f"\u2b07\ufe0f{round(float(list[2]),2)} Kilos",
                "text": {
                    "content": f"\u2b07\ufe0f{round(float(list[2]),2)} Kilos",
                },
                "type": "text"
            }
        ]
    }
        },)
    
    print('Weight Block Update: ',res.status_code)

def bmi_Fitness():
    
    list = weight_capture()

    bmi_diff = round((float(list[0]) - settings.BMI_GOAL),2)
 
    note = F'{bmi_diff} pts to go before status change'
    # TODO add this into the bmi patch - do this by page update.
    
    #connect to notion and update daily tracking data points for the latest day.
    pg_readurl = f'https://api.notion.com/v1/blocks/{settings.bmi_block_ID}'

    res = requests.request("PATCH",pg_readurl, headers = settings.headers,
                          json={
        "heading_1": {
        "text": [
            {
                "plain_text": f"\u2b07\ufe0f{round(float(list[0]),2)}",
                "text": {
                    "content": f"\u2b07\ufe0f{round(float(list[0]),2)}",
                },
                "type": "text"
            }
        ]
    }
        },)
    print('BMI Block Updated: ',res.status_code)

    pg_readurl = f'https://api.notion.com/v1/pages/{settings.BMI_PAGE_ID}'

    res = requests.request("PATCH",pg_readurl, headers = settings.headers, 
                       json = {
        "properties": {
            "Goal": {"number": round(float(list[0]),2)}}})
    
    print('BMI Goal Outcome Updated: ',res.status_code)
    
def body_fat_Fitness():
    
    list = weight_capture()
    
    #connect to notion and update daily tracking data points for the latest day.
    pg_readurl = f'https://api.notion.com/v1/blocks/{settings.body_fat_block_ID}'

    res = requests.request("PATCH",pg_readurl, headers = settings.headers,
                          json={
        "heading_1": {
        "text": [
            {
                "plain_text": f"\u2b07\ufe0f{round(float(list[1]),2)}%",
                "text": {
                    "content": f"\u2b07\ufe0f{round(float(list[1]),2)}%",
                },
                "type": "text"
            }
        ]
    }
        },)
    print('Body Fat Block Status: ',res.status_code)
    print('-------------------')

def notion_sleep_update():
    #connect to notion and update daily tracking data points for the latest day.
    list = sleep_capture()

    # TODO check if the date of the sleep date is as of today's date.  If it is not, then do not proceed with the update.
   
    notion_PageID = capture_notion_database_ID()

    pg_readurl = f'https://api.notion.com/v1/pages/{notion_PageID}'

    notion_databaseID = 'b32c01ae05114af282f309bf4337ac0c'

    res = requests.request("PATCH",pg_readurl, headers = settings.headers,
                          json={
        "parent": {"database_id": notion_databaseID},
        "properties": {
            'Awake Hour': {'number': int(list[0])+2},
            'Awake Minute': {'id': 'FDh%3D', 'type': 'number', 'number': int(list[1])},
            "To Sleep Hr. (1am = 13, 2am =14)": {'number': int(list[2])+12},
            "To Sleep Minute": {'number': int(list[3])},
            "Sleep Efficiency": {'number': float(list[4])}
            },
        },
    )
    print('Sleep Update: ',res.status_code)
