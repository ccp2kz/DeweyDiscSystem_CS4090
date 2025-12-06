import json
import logging
from kafka import KafkaConsumer
from pymongo import MongoClient

# Import config
try:
    from backend_config import config
except ImportError:
    from config import config

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("DeweyWorker")

def start_worker():
    #1.Connect to MongoDB (The Read Database)
    try:
        mongo_client = MongoClient(config.MONGO_URI)
        db = mongo_client[config.DATABASE_NAME]
        bags_collection = db['bags']
        logger.info("Connected to MongoDB.")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        return

    #2.Connect to Kafka
    try:
        consumer = KafkaConsumer(
            config.KAFKA_TOPIC_BAG_UPDATES,
            bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='bag-worker-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        logger.info(f"Listening to Kafka Topic: {config.KAFKA_TOPIC_BAG_UPDATES}")
    except Exception as e:
        logger.error(f"Failed to connect to Kafka: {e}")
        return

    #3.Process Messages Loop
    for message in consumer:
        try:
            event = message.value
            event_type = event.get("event_type")
            payload = event.get("payload")
            
            logger.info(f"Processing event: {event_type}")

            if event_type == "UserRegistered":
                # Create empty bag for new user
                user_id = payload['user_id']
                bags_collection.update_one(
                    {"user_id": user_id},
                    {"$setOnInsert": {"user_id": user_id, "discs": [], "updated_at": event['timestamp']}},
                    upsert=True
                )
                logger.info(f"Created bag for user {user_id}")

            elif event_type == "DiscAddedToBag":
                # Add disc to MongoDB document
                user_id = payload['user_id']
                disc_data = payload['disc_data']
                
                bags_collection.update_one(
                    {"user_id": user_id},
                    {"$push": {"discs": disc_data}, "$set": {"updated_at": event['timestamp']}},
                    upsert=True # Create if doesn't exist
                )
                logger.info(f"Added disc to user {user_id}'s bag")

            elif event_type == "DiscRemovedFromBag":
                # Remove disc from MongoDB document
                user_id = payload['user_id']
                disc_id = payload['disc_id']
                
                bags_collection.update_one(
                    {"user_id": user_id},
                    {"$pull": {"discs": {"id": disc_id}}, "$set": {"updated_at": event['timestamp']}}
                )
                logger.info(f"Removed disc {disc_id} from user {user_id}'s bag")
                
        except Exception as e:
            logger.error(f"Error processing message: {e}")

if __name__ == "__main__":
    start_worker()
