import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

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

    def append(self,range,data):
        sheet = self.service.spreadsheets()
        body_data = {"range": range, "majorDimension":'ROWS',"values": data}
        result = sheet.values().append(spreadsheetId=self.sheet_id,
                                        range=range, body=body_data, 
                                        valueInputOption='USER_ENTERED').execute()
        return
    
if __name__ == '__main__':
    G = googleHandler('1dVZlsgtbUq0MGWV4kBg7m6Kwv2kQtbBd88KFHq9uumo')
    values = G.read('Sheet1!A1')
    print(values)
    G.append('Session Tracker!A:C',[['Test2','Test22','Test222']])

