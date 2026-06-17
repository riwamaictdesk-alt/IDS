import pymongo
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDBConnection:
    """MongoDB Connection Handler"""
    
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            try:
                self._client = pymongo.MongoClient(Config.MONGODB_URI)
                self._db = self._client[Config.DATABASE_NAME]
                logger.info("MongoDB connected successfully")
            except Exception as e:
                logger.error(f"MongoDB connection failed: {e}")
                raise
    
    @property
    def db(self):
        return self._db
    
    def get_collection(self, collection_name):
        """Get a collection from the database"""
        return self._db[collection_name]
    
    def close(self):
        """Close the database connection"""
        if self._client:
            self._client.close()
            logger.info("MongoDB connection closed")
    
    def health_check(self):
        """Check if connection is alive"""
        try:
            self._client.admin.command('ping')
            return True
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
