from pprint import pprint
import os
from googleapiclient import discovery
from google.oauth2 import service_account
import requests
from itertools import chain
from dotenv import load_dotenv
load_dotenv(override=True)

try:
    scopes = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]
    secret_file = os.path.join(os.getcwd(), 'credentials2.json')

    spreadsheet_id = os.environ.get('SPREEDSHEET_ID')

    credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=scopes)
    service = discovery.build('sheets', 'v4', credentials=credentials)
    
    response = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='A:A').execute().get('values')
    comapnies_applied_set=set(map(str.lower,(chain.from_iterable(response))))

except OSError as e:
    print(e)

# Making a get request
response = requests.get('https://raw.githubusercontent.com/coderQuad/New-Grad-Positions-2023/master/README.md')
 
# print response
readme = response.text
i = readme.find('## The List')+13
table = readme[i:]

def checkIfExists(name:str,comapny_set):
    for i in comapny_set:
        if name.lower() in i or i in name.lower() or name.startswith('~') or name=='NOT FOUND':
            return True

    return False


def get_unapplied_companies(inp):
    not_applied=[]
    lines = inp.split('\n')
    keys=[]
    for i,l in enumerate(lines):
        if i==0:
            keys=[_i.strip() for _i in l.split('|')]
        elif i==1: 
            continue
        else:
            temp={keys[_i]:v.strip() for _i,v in enumerate(l.split('|')) if  _i>0 and _i<len(keys)-1}
            md_name = temp.get(keys[1],'NOT FOUND')
            name_end = md_name.find(']')
            name=md_name[1:name_end]
            if not checkIfExists(name,comapnies_applied_set):
                not_applied.append(name)
    return not_applied

unapplied = get_unapplied_companies(table)
print(f'Number of Unapplied comapnies: {len(unapplied)}')
print(get_unapplied_companies(table))