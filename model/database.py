import os
import pymongo
import pandas as pd
import json



client = pymongo.MongoClient("mongodb://localhost:27017/")
db_daily = client['daily']