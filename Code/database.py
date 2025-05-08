import gspread
from oauth2client.service_account import ServiceAccountCredentials
import universal


scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('', scope)
client = gspread.authorize(creds)

spreadsheet = client.open("lower")
spreadsheet2 = client.open("upper")
spreadsheet3 = client.open("full")
sheet = spreadsheet.sheet1
sheet2 = spreadsheet2.sheet1
sheet3 = spreadsheet3.sheet1

def check_col():
    headers = sheet.row_values(1)
    required_columns = ["Date","Type","Color","Pattern","Texture","Brand","Style","Season","Gender","Usage","TimeStamp"]
    missing_columns = [col for col in required_columns if col not in headers]

    if missing_columns:
        pass
    else:
        sheet.insert_row(required_columns, 1)

if universal.final_dict['upper'] != None:
    upper_values = list(universal.final_dict['upper'].values())
    upper_values = [universal.date]+ upper_values + [universal.time]
    print(upper_values)
    # check_col()
    sheet2.append_row(upper_values)
    # print('Inserted')

if universal.final_dict['lower'] != None:
    lower_values = list(universal.final_dict['lower'].values())
    lower_values = [universal.date]+ lower_values + [universal.time]
    print(lower_values)
    # check_col()
    sheet.append_row(lower_values)

if universal.final_dict['full'] != None:
    full_values = list(universal.final_dict['full'].values())
    full_values = [universal.date]+ full_values + [universal.time]
    print(full_values)
    # check_col()
    sheet3.append_row(full_values)

