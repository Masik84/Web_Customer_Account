import pandas as pd


data_file = '../DB_data.xlsx'

AM = pd.read_excel(data_file, sheet_name='AM_STL', usecols=['Sales_Grp',  'AM_name']).sort_values(by='AM_name')

STL = pd.read_excel(data_file, sheet_name='AM_STL', usecols=['STL'])
STL = STL.drop_duplicates(subset='STL').sort_values(by='STL')

LoB = pd.read_excel(data_file, sheet_name='AM_STL', usecols=['LoB'])
LoB = LoB.drop_duplicates(subset='LoB').sort_values(by='LoB')


Addresses = pd.read_excel(data_file,sheet_name='Addresses')

PaymentTerms = pd.read_excel(data_file,sheet_name='Cust_Data', usecols=['Pay_term', 'PT_description'])
PaymentTerms = PaymentTerms.drop_duplicates().sort_values(by='Pay_term')

YFRP = pd.read_excel(data_file,sheet_name='Cust_Data', usecols=['YFRP'])
YFRP = YFRP.drop_duplicates().sort_values(by='YFRP')
YFRP = YFRP[~YFRP['YFRP'].isnull()]


# YFRP
# Customers
# ShipTos
# Addresses

print(LoB)


Prod_Sub_Class = pd.read_excel(data_file, sheet_name='Product_Data', usecols=['Sub_Class', 'Sub_Class_Name'])
Prod_Sub_Class = Prod_Sub_Class.drop_duplicates().sort_values(by='Sub_Class')

Sal_Prod = pd.read_excel(data_file, sheet_name='Product_Data', usecols=['Sal_Prod_Code', 'Sal_Prod_Name'])
Sal_Prod = Sal_Prod.drop_duplicates().sort_values(by='Sal_Prod_Name')

Prod_Status = pd.read_excel(data_file, sheet_name='Product_Data', usecols=['Status_code', 'Status_descr'])
Prod_Status = Prod_Status.drop_duplicates().sort_values(by='Status_code')