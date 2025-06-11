import os
from tinydb import TinyDB
from MQTT.serializer import serializer

def find_dispenser() -> list:
    """Find all devices in the database."""
    # Define the database connector
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('dispenser')
    # Search the database for all devices that are active
    result = db_connector.all()
    
    # The result is a list of dictionaries, we only want the device names
    if result:
        result = [x["dispenser"] for x in result]
    
    return result

def find_temperature() -> list:
    """Find all devices in the database."""
    # Define the database connector
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('temperature')
    # Search the database for all devices that are active
    result = db_connector.all()
    
    # The result is a list of dictionaries, we only want the device names
    if result:
        result = [x["temperature"] for x in result]
    
    return result
def find_ground_truth() -> list:
    """Find all devices in the database."""
    # Define the database connector
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('ground_Truth')
    # Search the database for all devices that are active
    result = db_connector.all()
    
    # The result is a list of dictionaries, we only want the device names
    if result:
        result = [x["ground_Truth"] for x in result]
    
    return result

def find_drop_oscillation() -> list:
    """Find all devices in the database."""
    # Define the database connector
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('drop_oscillation')
    # Search the database for all devices that are active
    result = db_connector.all()
    
    # The result is a list of dictionaries, we only want the device names
    if result:
        result = [x["drop_oscillation"] for x in result]
    
    return result

def find_recipe() -> list:
    """Find all devices in the database."""
    # Define the database connector
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('recipe')
    # Search the database for all devices that are active
    result = db_connector.all()
    
    # The result is a list of dictionaries, we only want the device names
    if result:
        result = [x["recipe"] for x in result]
    
    return result

def find_final_weight() -> list:
    """Find all devices in the database."""
    # Define the database connector
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('final_weight')
    # Search the database for all devices that are active
    result = db_connector.all()
    
    # The result is a list of dictionaries, we only want the device names
    if result:
        result = [x["final_weight"] for x in result]
    
    return result
#if __name__ == "__main__":
