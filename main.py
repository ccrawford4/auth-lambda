import os
import uuid

import certifi
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from fastapi import FastAPI

load_dotenv()
uri = os.environ.get('MONGO_CONNECTION_STRING')
db_name = os.environ.get('MONGO_DB_NAME')

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'), tlscafile=certifi.where())
database = client[db_name]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
except Exception as e:
    print(e)
    print("Could not create server.")
    exit(1)

app = FastAPI()

@app.get("/login/{tenant_name}")
async def login(tenant_name: str) :
    collection = database["tenants"]
    try :
        query = { "name" : tenant_name }
        result = collection.find_one(query)
        if not result :
            return {"status": 404, "message": f'{tenant_name} not found!', "error": "Not Found"}
        return {"status": 200, "message": f'{tenant_name} logged in!', "data": result}
    except Exception as e:
        return { "status": 500, "message": "Internal Server Error!", "error": str(e)}

@app.post("/register/{tenant_name}")
async def register(tenant_name: str):
    try :
        collection = database["tenants"]
        data = {
            '_id': uuid.UUID(),
            'name': tenant_name,
        }
        collection.insert_one(data)
        return {"status": 200, "message": "Successfully Registered", "error": None}
    except Exception as e:
        return {"status": 500, "message": "Internal Server Error", "error": str(e)}