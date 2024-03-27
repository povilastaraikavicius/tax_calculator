from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Dict, List
from datetime import datetime, timedelta

def connect_to_mongodb(host: str, port: int, db_name: str) -> Database:
    client = MongoClient(host, port)
    database = client[db_name]
    return database

def find_documents(collection: Collection, query: Dict, limit: int) -> List[Dict]:
    documents = collection.find(query).limit(limit)
    return list(documents)

def calculate_tax_return(income: float) -> Dict:
   
    GPM_tax_rate = 0.20
    health_tax_rate = 0.15

    gpm_tax = income * GPM_tax_rate
    income_left = income - gpm_tax
    health_tax = income_left * health_tax_rate
    total_tax = gpm_tax + health_tax
    net_income = income - total_tax

    return {
        "GPM_tax": gpm_tax,
        "health_tax": health_tax,
        "total_tax": total_tax,
        "net_income": net_income
    }

def main():
    
    mongodb_host = 'localhost'
    mongodb_port = 27017
    database_name = 'tax_calculator'
    collection_name = 'Persons'

    
    db = connect_to_mongodb(mongodb_host, mongodb_port, database_name)

    
    collection = db[collection_name]

    
    min_age = 20
    max_age = 50
    max_birth_date = datetime.now() - timedelta(days=min_age*365)
    min_birth_date = datetime.now() - timedelta(days=max_age*365)

    
    query = {"date of birth": {"$gte": min_birth_date, "$lte": max_birth_date}}

   
    results = find_documents(collection, query, limit=10)
    
    print("Matching documents:")
    for idx, result in enumerate(results, start=1):
        print(f"{idx}. {result['name']} {result['surname']} (Age: {result['age']})")

    
    selected_option = None
    while selected_option is None:
        try:
            selected_option = int(input("Choose an option by entering the corresponding number: "))
            if selected_option < 1 or selected_option > len(results):
                raise ValueError
        except ValueError:
            print("Invalid option. Please enter a number corresponding to one of the options.")
            selected_option = None

    
    selected_document = results[selected_option - 1]
    print("Selected document:")
    print(selected_document)

    
    tax_return = calculate_tax_return(selected_document["salary"])

    
    tax_card = {
        "person_name": selected_document["name"],
        "person_surname": selected_document["surname"],
        "age": selected_document["age"],
        "salary": selected_document["salary"],
        "GPM_tax": tax_return["GPM_tax"],
        "health_tax": tax_return["health_tax"],
        "total_tax": tax_return["total_tax"],
        "net_income": tax_return["net_income"]
    }

    print("Tax card:")
    print(tax_card)

if __name__ == "__main__":
    main()
