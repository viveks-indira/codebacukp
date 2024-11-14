# import logging
# from logging.handlers import RotatingFileHandler
# import os
#
# # Define where you want to store the logs (this should be a directory)
# LOG_DIR = r'E:\\Superset\\apache_project\\logs'  # This should point to a directory, not a log file
#
# # Create the log directory if it doesn't exist
# if not os.path.exists(LOG_DIR):
#     os.makedirs(LOG_DIR)
#
# # Now define the log file name
# LOG_FILE = os.path.join(LOG_DIR, 'superset.log')
#
# # Set up logging to write logs to a specific file
# file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5000000, backupCount=10)
# file_handler.setLevel(logging.INFO)  # Change to DEBUG for more verbose logging
# file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
#
# # Add handler to root logger
# logging.getLogger().addHandler(file_handler)
# logging.getLogger().setLevel(logging.INFO)
#
# # Other configurations
# SECRET_KEY = '/X3ICyIAxS2aWnVEx/63uz1DdQIcJAz6alQSmBJxxDRd00YJOWd19lxR'
# SQLALCHEMY_ENCRYPTION_KEY = 'Ebe2sz9f8s6tNfin8pIzziLyCLZAyiRwgfOE8QT71MW8zTSseNJunKOp'
import logging
from logging.handlers import RotatingFileHandler
import os

# Define where you want to store the logs (this should be a directory)
LOG_DIR = r'E:\\Superset\\apache_project\\logs'  # This should point to a directory

# Create the log directory if it doesn't exist
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Now define the log file name
LOG_FILE = os.path.join(LOG_DIR, 'superset.log')

# Set up logging to write logs to a specific file
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5000000, backupCount=10)
file_handler.setLevel(logging.INFO)  # Change to DEBUG for more verbose logging
file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))

# Add handler to root logger
logging.getLogger().addHandler(file_handler)
logging.getLogger().setLevel(logging.INFO)

# Other configurations
SECRET_KEY = '/X3ICyIAxS2aWnVEx/63uz1DdQIcJAz6alQSmBJxxDRd00YJOWd19lxR'
SQLALCHEMY_ENCRYPTION_KEY = 'Ebe2sz9f8s6tNfin8pIzziLyCLZAyiRwgfOE8QT71MW8zTSseNJunKOp'
SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://root:root@localhost/dbs?driver=ODBC+Driver+17+for+SQL+Server'


# Custom error handling for decryption
def handle_decryption():
    try:
        # Example of some database operation that uses decryption
        # (This part would depend on how your application attempts to decrypt values)
        pass  # Replace with actual decryption logic

    except ValueError as e:
        logging.error(f"Decryption error: {str(e)}. Please check the SQLALCHEMY_ENCRYPTION_KEY.")

    except UnicodeDecodeError as e:
        logging.error(f"Unicode decode error during decryption: {str(e)}. Please verify your encryption key and data.")


# Call the decryption handling function
handle_decryption()
