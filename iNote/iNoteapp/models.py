from pymongo import MongoClient
from django.conf import settings

conn = MongoClient(settings.MONGODB_ATLAS_URI)