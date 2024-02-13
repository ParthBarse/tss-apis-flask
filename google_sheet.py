import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('creds_google_apis.json', scope)
client = gspread.authorize(creds)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1ITTXXyXV0Bj8UpKqm37ULpW7WjctwCu7AIagfoUF8KA/edit'
sheet = client.open_by_url(spreadsheet_url)
sheet_instance_1 = sheet.get_worksheet(0)
sheet_instance_2 = sheet.get_worksheet(1)
sheet_instance_3 = sheet.get_worksheet(2)
sheet_instance_4 = sheet.get_worksheet(3)
sheet_instance_5 = sheet.get_worksheet(4)
sheet_instance_6 = sheet.get_worksheet(5)
products = sheet_instance_1.get_all_records(head=1)
discount = sheet_instance_2.get_all_records(head=1)
colors = sheet_instance_3.get_all_records(head=1)
variants = sheet_instance_4.get_all_records(head=1)
size = sheet_instance_5.get_all_records(head=1)
seoArea = sheet_instance_6.get_all_records(head=1)
all_products = []
for product in products:
    p_temp = {}
    pid = product["pid"]
    p_temp['pid'] =  product["pid"]
    for key in product:
        p_temp[key] = product[key]
    for i in discount:
        if i['pid'] == pid:
            p_temp['discount'] = i['discount']
            p_temp['discount_date'] = {"start":i['start'], "end":i["end"]}
            p_temp['discount_type'] = i['discount_type']
    temp_colors = []
    for j in colors:
        if j['pid'] == pid:
            temp_colors.append(j)
        p_temp['colors'] = temp_colors
    temp_variants = []
    for k in variants:
        if k["pid"] == pid:
            if k['GalleryImg']:
                k['GalleryImg'] = k['GalleryImg'].split(",")
            temp_variants.append(k)
        p_temp['variants'] = temp_variants
    temp_size = []
    for x in size:
        if x['pid'] == pid:
            temp_size.append(x)
        p_temp['size']=temp_size
    for y in seoArea:
        if y['pid'] == pid:
            p_temp['SEOArea'] = y
    all_products.append(p_temp)
print(all_products)
