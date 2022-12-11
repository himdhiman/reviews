from django.conf import settings
import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(settings.CRED_PATH, scope)
client = gspread.authorize(creds)

sheet_orders = client.open("Interakt Orders - For Reviews")
sheet_review = client.open("Interakt Reviews Data")

def get_data():
    sheet_instance = sheet_review.get_worksheet(0)
    data = sheet_instance.get_all_records()
    print(data)
    return data

# # Extract and print all of the values
# list_of_hashes = sheet.get_all_records()
# print(list_of_hashes)
