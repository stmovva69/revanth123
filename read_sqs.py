# import boto3
# import hashlib
# import json
# import os
# import psycopg2
# from datetime import datetime
#
# # Set mock AWS credentials
# os.environ['AWS_ACCESS_KEY_ID'] = 'mock_access_key'
# os.environ['AWS_SECRET_ACCESS_KEY'] = 'mock_secret_key'
# os.environ['AWS_SESSION_TOKEN'] = 'mock_session_token'
#
# # SQS configuration
# sqs_client = boto3.client('sqs', endpoint_url='http://localhost:4566', region_name='us-east-1')
# queue_url = 'http://localhost:4566/000000000000/login-queue'
#
#
# # Mask PII and write to PostgreSQL
# def mask_data(data):
#     if 'device_id' in data and 'ip' in data:
#         hashed_device_id = hashlib.md5(data['device_id'].encode()).hexdigest()
#         hashed_ip = hashlib.md5(data['ip'].encode()).hexdigest()
#         data['masked_device_id'] = hashed_device_id
#         data['masked_ip'] = hashed_ip
#         del data['device_id']
#         del data['ip']
#
#     return data
#
#
# def write_to_postgres(data):
#     connection = psycopg2.connect(
#         host="localhost",
#         port="5432",
#         dbname="postgres",
#         user="postgres",
#         password="postgres"
#     )
#
#     cursor = connection.cursor()
#
#     # Create the user_logins table if it doesn't exist
#     cursor.execute("""
#             CREATE TABLE IF NOT EXISTS user_logins (
#                 id SERIAL PRIMARY KEY,
#                 user_id VARCHAR(255),
#                 device_type VARCHAR(255),
#                 masked_ip VARCHAR(255),
#                 masked_device_id VARCHAR(255),
#                 locale VARCHAR(255),
#                 app_version VARCHAR(255),
#                 create_date TIMESTAMP
#             )
#         """)
#     connection.commit()
#
#     for record in data:
#         create_date = record.get('create_date', '2023-01-01')
#         cursor.execute(
#             """
#             INSERT INTO user_logins(user_id, device_type
#             , masked_ip, masked_device_id, locale, app_version, create_date)
#             VALUES(%s, %s, %s, %s, %s, %s, %s)
#             """,
#             (record['user_id'], record['device_type'],
#              record['masked_ip'], record['masked_device_id'],
#              record['locale'], record['app_version'],
#              create_date)
#         )
#     connection.commit()
#     cursor.close()
#     connection.close()
#
#
# # Read messages from SQS, mask PII, and write to PostgreSQL
# def process_sqs_messages():
#     messages = sqs_client.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=20)
#     data_to_write = []
#     for message in messages.get('Messages', []):
#         message_body = message['Body']
#         login_data = json.loads(message_body)
#         masked_login_data = mask_data(login_data)
#
#         # Conditionally add 'create_date' field if it doesn't exist
#         if 'create_date' not in masked_login_data:
#             masked_login_data['create_date'] = datetime.now().isoformat()
#
#         data_to_write.append(masked_login_data)
#     write_to_postgres(data_to_write)
#
#
# if __name__ == "__main__":
#     process_sqs_messages()

import boto3
import hashlib
import json
import os
import psycopg2
from datetime import datetime

# Set mock AWS credentials
os.environ['AWS_ACCESS_KEY_ID'] = 'mock_access_key'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'mock_secret_key'
os.environ['AWS_SESSION_TOKEN'] = 'mock_session_token'

# SQS configuration
sqs_client = boto3.client('sqs', endpoint_url='http://localhost:4566', region_name='us-east-1')
queue_url = 'http://localhost:4566/000000000000/login-queue'


# Mask PII and write to PostgreSQL
def mask_data(data):
    if 'device_id' in data and 'ip' in data:
        hashed_device_id = hashlib.md5(data['device_id'].encode()).hexdigest()
        hashed_ip = hashlib.md5(data['ip'].encode()).hexdigest()
        data['masked_device_id'] = hashed_device_id
        data['masked_ip'] = hashed_ip
        del data['device_id']
        del data['ip']

    # Replace None values with 'NULL'
    for key, value in data.items():
        if value is None:
            data[key] = 'NULL'

    return data


def write_to_postgres(data):
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="postgres",
        user="postgres",
        password="postgres"
    )

    cursor = connection.cursor()

    # Create the user_logins table if it doesn't exist
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_logins (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255),
                device_type VARCHAR(255),
                masked_ip VARCHAR(255),
                masked_device_id VARCHAR(255),
                locale VARCHAR(255),
                app_version VARCHAR(255),
                create_date TIMESTAMP
            )
        """)
    connection.commit()

    for record in data:
        # Handle missing keys by setting default values
        user_id = record.get('user_id', 'NULL')
        device_type = record.get('device_type', 'NULL')
        masked_ip = record.get('masked_ip', 'NULL')
        masked_device_id = record.get('masked_device_id', 'NULL')
        locale = record.get('locale', 'NULL')
        app_version = record.get('app_version', 'NULL')
        create_date = record.get('create_date', datetime.now().isoformat())

        cursor.execute(
            """
            INSERT INTO user_logins(user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
            VALUES(%s, %s, %s, %s, %s, %s, %s)
            """,
            (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
        )
    connection.commit()
    cursor.close()
    connection.close()


# Read messages from SQS, mask PII, and write to PostgreSQL
def process_sqs_messages():
    messages = sqs_client.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=5000)
    data_to_write = []
    for message in messages.get('Messages', []):
        message_body = message['Body']
        login_data = json.loads(message_body)
        masked_login_data = mask_data(login_data)

        # Conditionally add 'create_date' field if it doesn't exist
        if 'create_date' not in masked_login_data:
            masked_login_data['create_date'] = datetime.now().isoformat()

        data_to_write.append(masked_login_data)
    write_to_postgres(data_to_write)


if __name__ == "__main__":
    process_sqs_messages()
