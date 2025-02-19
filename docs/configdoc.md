## Src - Aquasensor_Backend - cache.py

# Cache URL /
Default: os.getenv("CACHE_URL", "memory://")
Required: Yes
Function: defines the location and type of cache that will be used by the application

## Src - Aquasensor_backend - sensors.py

# API_BASE_URL
Default: none
Required: yes
Function:This is the base URL of the external API that the application interacts with. It specifies the root URL for making API requests


# API_API_KEY
Default: none
Required: yes
Function: This is the API key used for authentication when making requests to the external API specified in API_BASE_URL. It ensures that only authorized users or services can access the API and retrieve or send data.



## Src - Aquasensor_backend - mail.py

# SMTP_SERVER
Default: none
Required: yes
Function: This specifies the address of the SMTP server that will handle sending the email. 

# SMTP_PORT
Default: none
Required: yes
Function: his specifies the port number used for the SMTP connection. Port 465 is used for SSL connections, while port 587 is used for TLS connections. The port defines the communication method used to securely send the email.

# EMAIL_SENDER
Default: none
Required: yes
Function: This is the email address of the sender. It is used for authentication and as the "From" field in the email message.

# EMAIL_PASSWORD
Default: none
Required: yes
Function: his is the password for the email account specified in EMAIL_SENDER. It's used to authenticate the sender's email account with the SMTP server, ensuring only authorized users can send emails from that account.

## Src - Aquasensor backend - mqtt.py

# Database URL  /
Default: os.getenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
Required: Yes
Function: used to specify the location and configuration of the database that the application will connect to. If the environment variable is not set, it defaults to an in-memory SQLite database

# Database echo /
Default: bool(os.getenv("DATABASE_ECHO", False))
Required: No
Function: is used to control whether SQLAlchemy should log the SQL queries it generates and sends to the database.  If it's not set, it defaults to False, meaning that SQL queries will not be printed to the console.

# Jinja Templated DIR /
Default: os.getenv("JINJA_TEMPLATES_DIR", "./src/frontend")
Required: No
Function: defines the directory path where Jinja2 templates are located. It is used to set the location of the templates that will be rendered by the FastAPI application.


## mqtt Configs

# DB_URL /
Default: none
Required: Yes
Function: Retrieves the URL of the InfluxDB instance from the environment variable INFLUXDB_URL. This URL is used to connect to the InfluxDB server.

# DB_Token /
Default: none
Required: Yes
Function: Retrieves the authentication token for InfluxDB from the environment variable INFLUXDB_TOKEN. This token is used to authenticate the client when making requests to the InfluxDB server.

# DB_ORG /
Default: none
Required: Yes
Function:  Retrieves the organization name from the environment variable INFLUXDB_ORG. This is used to specify the InfluxDB organization when writing data.

# DB_BUCKET /
Default: none
Required: Yes
Function: Retrieves the bucket name from the environment variable INFLUXDB_BUCKET. This specifies the InfluxDB bucket (database container) where sensor data will be written.

# DB_BROKER /
Default: none
Required: Yes
Function: Retrieves the MQTT broker address from the environment variable MQTT_BROKER. This is the address of the MQTT server to which the client will connect to subscribe and publish messages.

## Api Middleware - functions.py

# USERNAME
Default: none
Required: Yes
Function: This is a unique identifier used to authenticate against the AquaSensor system.

# TOKEN
Default: none
Required: Yes
Function: This is a secret key used in conjunction with the username to authenticate API requests. It ensures that only authorized users can access the data.