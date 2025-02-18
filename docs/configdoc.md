# API Username
Default: Requires being Set
Required: Yes
Function:  used to authenticate or identify the user making the request to the AquaSensor API. If the AQUASENSOR_USERNAME environment variable is not set, the assert USERNAME statement will raise an error, indicating that the username must be provided.

# API Token
Default: Requires being set
Required: Yes
Function:  used to authenticate or authorize the user when making requests to the AquaSensor API. If the AQUASENSOR_TOKEN environment variable is not set, the assert TOKEN statement will raise an error, indicating that the token must be provided.

# Cache URL
Default: os.getenv("CACHE_URL", "memory://")
Required: Yes
Function: defines the location and type of cache that will be used by the application

# Database URL  
Default: os.getenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
Required: Yes
Function: used to specify the location and configuration of the database that the application will connect to. If the environment variable is not set, it defaults to an in-memory SQLite database

# Database echo
Default: bool(os.getenv("DATABASE_ECHO", False))
Required: No
Function: is used to control whether SQLAlchemy should log the SQL queries it generates and sends to the database.  If it's not set, it defaults to False, meaning that SQL queries will not be printed to the console.

# Password Salt
Default: getenv("PASSWORD_SALT") or "AQUASENSOR"
Required: Yes
Function: used as a salt value when hashing passwords to enhance security. It is intended to add an additional layer of randomness to the password hashing process, preventing attackers from using precomputed hash tables (like rainbow tables) to easily reverse the hashed passwords.

# Jinja Templated DIR
Default: os.getenv("JINJA_TEMPLATES_DIR", "./src/frontend")
Required: No
Function: defines the directory path where Jinja2 templates are located. It is used to set the location of the templates that will be rendered by the FastAPI application.