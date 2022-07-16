import csv
from datetime import datetime
import os
import pandas as pd



now = datetime.today().strftime('%Y-%m-%d')
fx_usd_file = 'Exchange_rate_USD' + '_' + now + '.csv'
fx_eur_file = 'Exchange_rate_EUR' + '_' + now + '.csv'

date_from = '01/01/2020'
date_to = datetime.today().strftime('%d/%m/%Y')
usd_id = 'R01235'
eur_id = 'R01239'

url_usd = f"http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={date_from}&date_req2={date_to}&VAL_NM_RQ={usd_id}"

fx_usd_df = pd.read_xml(url_usd)
fx_usd_df = fx_usd_df.stack().str.replace(',', '.').unstack()
fx_usd_df.to_csv(fx_usd_file, sep=';', encoding='utf-8', index=False, date_format='%Y-%m-%d', header=False)
print('Файл обновлен')

with open(fx_usd_file, 'r', encoding='utf-8') as f:
    fields = ['Date', 'Curr_code', 'Nominal', 'Rate']
    reader = csv.DictReader(f, fields, delimiter=';')
    
    data_for_upload = []
    for row in reader:
        row['Date'] = datetime.strptime(row['Date'], '%d.%m.%Y')
        print(type(row['Date']))