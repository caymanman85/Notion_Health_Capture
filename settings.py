# Fitness Syncer 
API_ENDPOINT = 'https://www.fitnesssyncer.com/api/oauth/access_token'

CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'https://personal.fitnesssyncer.com/'

Huawei_Activity = '0dc47184-649c-41b7-b4d2-bc8d9e2b0594' 
Huawei_Sleep = '2990b261-7242-4538-8e38-5659c58f54a5'
Huawei_Weight = '76401ca9-46ff-44b1-be2b-536f7fb2f7fb'

DATA_SOURCES = [Huawei_Weight,Huawei_Sleep,Huawei_Activity]

RETRIES=20
API_REFRESH_ENDPOINT = 'https://api.fitnesssyncer.com/api/syncs/'
API_SYNC_ENDPOINT = 'https://api.fitnesssyncer.com/api/syncs/'
url = f'https://www.fitnesssyncer.com/api/oauth/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope=sources&state=Informationforyourservice'
sleep_data_source_id = f'https://api.fitnesssyncer.com/api/providers/sources/{Huawei_Sleep}/items/'
weight_data_source_id = f'https://api.fitnesssyncer.com/api/providers/sources/{Huawei_Weight}/items/'
activity_data_source_id = f'https://api.fitnesssyncer.com/api/providers/sources/{Huawei_Activity}/items/'

data_source_id = 'https://api.fitnesssyncer.com/api/oauth/access_token'

code = ''

data_headers = {
    'content-type': 'application/x-www-form-urlencoded',
    "Authorization": "Bearer " + code
}

# Notion
notion_token = ''
notion_databaseID = 'b32c01ae05114af282f309bf4337ac0c'

weight_block_ID = '7d751bf1032c4705be2adc8d88d59e2a'

bmi_block_ID = 'f59800ea778e4b5abe811cf3f831ae32'
BMI_PAGE_ID = 'c6e38599d9874fe78120bb99938d49a3'
bodyfat_block_ID = 'd98015d3718f45918049e22311ede563'

BMI_GOAL = 22

db_headers = {
    "Authorization": "Bearer " + notion_token,
    "Notion-Version": "2021-08-16"
}

headers = {
    "Authorization": "Bearer " + notion_token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16"
}

bmi_block_ID = 'f59800ea778e4b5abe811cf3f831ae32'
BMI_GOAL_BLOCK_ID = 'c6e38599d9874fe78120bb99938d49a3'
weight_block_ID = '7d751bf1032c4705be2adc8d88d59e2a'
WEIGHT_GOAL_BLOCK_ID = '3779ae17b3ea4225908fbad6aeef8c81'
WEIGHT_GOAL_BLOCK_ID_2 = '2f65907aee2d40afa6de1dd6311f4b72'
body_fat_block_ID = 'd98015d3718f45918049e22311ede563'