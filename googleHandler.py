import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pprint import pprint

class googleHandler:
    def __init__(self, sheet_id):
        self.SCOPES = ["https://www.googleapis.com/auth/drive"]
        self.sheet_id = sheet_id
        self.get_credentials()

    def get_credentials(self):
        creds = None
        if os.path.exists('config/token.pickle'):
            with open('config/token.pickle','rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'config/google-keys.json', self.SCOPES)
                creds = flow.run_local_server()
            with open('config/token.pickle','wb') as token:
                pickle.dump(creds,token)
        self.service = build('sheets','v4',credentials=creds)

    def read(self, range):
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.sheet_id,
                                    range=range).execute()
        values = result.get('values',[])

        if not values:
            return ''
        else:
            return values
    def write(self, range_, data):
        sheet = self.service.spreadsheets()
        body_data = {"range": range_, "majorDimension":'ROWS',"values": data}
        request = sheet.values().update(spreadsheetId=self.sheet_id,
                                        range=range_,body=body_data,
                                        valueInputOption='USER_ENTERED')
        response = request.execute()
        return
    def append(self,range,data):
        sheet = self.service.spreadsheets()
        body_data = {"range": range, "majorDimension":'ROWS',"values": data}
        request = sheet.values().append(spreadsheetId=self.sheet_id,
                                        range=range, body=body_data, 
                                        valueInputOption='USER_ENTERED')
        response = request.execute()
        return

    def add_column(self, subsheetId):
        sheet = self.service.spreadsheets()
        body_data = { 
            "requests": [{
                    "appendDimension": {
                        "sheetId":subsheetId,
                        "dimension":"COLUMNS",
                        "length":1
                    }
            }],
            "includeSpreadsheetInResponse":False,
            "responseRanges":"",
            "responseIncludeGridData":False
        }
        request = sheet.batchUpdate(spreadsheetId=self.sheet_id, body=body_data)
        response = request.execute()
        return

    def get_sheet_id(self):
        sheet = self.service.spreadsheets()


if __name__ == '__main__':
    G = googleHandler('1dVZlsgtbUq0MGWV4kBg7m6Kwv2kQtbBd88KFHq9uumo')
    values = G.read('Sheet1!A1')
    G.write('Sheet1!A1', [['B']])
    G.add_column(2128905475)
    print(values)
    G.append('Session Tracker!A:C',[['Test2','Test22','Test222']])

