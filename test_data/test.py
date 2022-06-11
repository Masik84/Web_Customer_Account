import pandas as pd
from faker import Faker

fake = Faker('ru_RU')

def fake_companies(num_rows=569):
    companies = []
    for _ in range(num_rows):
        companies.append([fake.large_company()]
        )
    return companies

def fake_addresses(num_rows=4642):
    address = []
    for _ in range(num_rows):
        address.append([fake.ad()]
        )
    return address

if __name__ == '__main__':
    companies = fake_companies()
    print(companies)
    df = pd.DataFrame(companies)
    writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='welcome', index=False)
    writer.save()
