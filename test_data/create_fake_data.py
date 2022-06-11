import pandas as pd
from datetime import date
import random
from faker import Faker


fake = Faker('ru_RU')


#Функция, создающая компании
# Создадим список, в котором каждый вложенный список - компания:
def fake_companies(num_rows=569):
    companies = []
    for _ in range(num_rows):
        companies.append([fake.large_company()]
        )
    return companies


# Функция, создающая сотрудников
# При сложении двух списков мы объединяем их содержимое в общий список. 
# Т.е. в результате работы этого кода мы получим список со 100 списками 
# внутри, в каждом из которых будет информация о компании и сотруднике:

def fake_employees(companies, num_rows=10):
    employees = []
    for company in companies:
        for _ in range(num_rows):
            employee = [fake.name(), fake.job(), fake.phone_number(),
                fake.free_email()]
            employees.append(company + employee)
    return employees 


 # Функция, создающая платежи
 # По аналогии создадим платежи за 12 месяцев
def fake_payments(employees):
    payments = []
    for employee in employees:
        for month in range(1, 13):
            payment_date = date(2020, month, random.randint(10, 29))
            ammount = random.randint(20000, 200000)
            payment = [payment_date, ammount]
            payments.append(employee + payment)
    return payments



def generate_data(payments):
    with open('payments.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        for payment in payments:
            writer.writerow(payment)




if __name__ == '__main__':
    companies = fake_companies()
    employees = fake_employees(companies)
    payments = fake_payments(employees)
    generate_data(payments)