Reading Messages from the Queue
The application utilizes the boto3 library to interact with an Amazon SQS queue. It continuously retrieves messages from the SQS queue using the receive_message method. The maximum number of messages retrieved per batch is specified using the MaxNumberOfMessages parameter. The retrieved messages are processed and written to a PostgreSQL database.

Data Structures
The application processes JSON messages received from the SQS queue. Each message contains login data, which is stored as a dictionary (JSON object). This dictionary is then manipulated to mask sensitive PII data, and the processed data is written to the PostgreSQL database.

Masking PII Data
Sensitive PII (Personally Identifiable Information) data, such as device IDs and IP addresses, is masked using MD5 hashing. Hashing ensures that duplicate values can be identified without storing the original sensitive data. The masked device ID and IP address are added to the processed data, and the original device ID and IP address are removed.

Connecting and Writing to Postgres
The application establishes a connection to a PostgreSQL database using the psycopg2 library. It creates a cursor to execute SQL queries. A table named user_logins is created if it doesn't already exist. Processed login data is then inserted into this table using parameterized queries to prevent SQL injection vulnerabilities.

Application Execution
To run the application:

Set the mock AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN) as environment variables.
Configure the SQS client with the appropriate endpoint URL and region.
Adjust the queue_url to match the SQS queue URL.
Install the required Python libraries (boto3, psycopg2) using pip install boto3 psycopg2.
Run the script, which will continuously retrieve messages from the SQS queue, mask PII data, and write it to the PostgreSQL database.
It's recommended to run the application on a server or cloud instance to ensure continuous message processing and data storage.Reading Messages from the Queue
The application utilizes the boto3 library to interact with an Amazon SQS queue. It continuously retrieves messages from the SQS queue using the receive_message method. The maximum number of messages retrieved per batch is specified using the MaxNumberOfMessages parameter. The retrieved messages are processed and written to a PostgreSQL database.

Data Structures
The application processes JSON messages received from the SQS queue. Each message contains login data, which is stored as a dictionary (JSON object). This dictionary is then manipulated to mask sensitive PII data, and the processed data is written to the PostgreSQL database.

Masking PII Data
Sensitive PII (Personally Identifiable Information) data, such as device IDs and IP addresses, is masked using MD5 hashing. Hashing ensures that duplicate values can be identified without storing the original sensitive data. The masked device ID and IP address are added to the processed data, and the original device ID and IP address are removed.

Connecting and Writing to Postgres
The application establishes a connection to a PostgreSQL database using the psycopg2 library. It creates a cursor to execute SQL queries. A table named user_logins is created if it doesn't already exist. Processed login data is then inserted into this table using parameterized queries to prevent SQL injection vulnerabilities.

Application Execution
To run the application:

Set the mock AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN) as environment variables.
Configure the SQS client with the appropriate endpoint URL and region.
Adjust the queue_url to match the SQS queue URL.
Install the required Python libraries (boto3, psycopg2) using pip install boto3 psycopg2.
Run the script, which will continuously retrieve messages from the SQS queue, mask PII data, and write it to the PostgreSQL database.
It's recommended to run the application on a server or cloud instance to ensure continuous message processing and data storage.