# Create an income tax calculator: 
#  - Generate at least 500 documents , with fields: name, surname, date of birth , age (determined from date of birth), anual salary before tax (EUR, round to 2 numbers after comma)
#  - Create a CLI application that would let us get first 10 people from database within the age bracket [min_age, max_age]
#  - Those people name surname and age should be shown as an option to choose.
#  - When one of ten options is chosen, there should be calculated tax return (it should be created a document as a tax card, values taken from database). Lets say GPM tax is 20% and HealtTax is 15% from 90% of the income left after GPM deduction.
#  - The final values should be show and wrriten to database (like a generated data and taxes paid, take home pay etc.) and portrayed in a web page (use flask and docker, show the url were to click )


from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Dict, List
from faker import Faker
from random import randint
from datetime import datetime, timedelta



def connect_to_mongodb(host: str, port: int, db_name: str) -> Database:
    client = MongoClient(host, port)
    database = client[db_name]
    return database


def insert_document(collection: Collection, document: Dict) -> str:
    result = collection.insert_one(document)
    print(f"Printed result: {result}")
    return str(result.inserted_id)


def create_a_person(fake: Faker) -> Dict:
    name = fake.first_name()
    surname = fake.last_name()
    max_age = datetime.now() - timedelta(days=18*365)
    min_age = datetime.now() - timedelta(days=75*365)
    date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=75)  
    
    date_of_birth_datetime = datetime.combine(date_of_birth, datetime.min.time())
    age = int((datetime.now() - date_of_birth_datetime).days // 365.25) 
    salary = randint(1500, 5000)
    return name, surname, age, date_of_birth_datetime, salary




if __name__ == "__main__":
    mongodb_host = "localhost"
    mongodb_port = 27017
    database_name = "tax_calculator"
    collection_name = "Persons"

    db = connect_to_mongodb(mongodb_host, mongodb_port, database_name)

    collection = db[collection_name]
    fake = Faker()

    for _ in range(500):
        name, surname, age, date_of_birth, salary = create_a_person(fake)  
        document = {
            "name": name,
            "surname": surname,
            "age": age,
            "date of birth": date_of_birth,
            "salary" : salary
        }
        inserted_id = insert_document(collection, document)
        print(f"Inserted document with ID: {inserted_id}")
        print(f"This person was inserted into the database: {document}")
