from dotenv import load_dotenv
from urllib.parse import urlparse
import logging
import psycopg2
import os

load_dotenv()

connection = None
database = None

def db_file(filepath, *args):
  """
  Reads a file and returns the contents as a string.
  For now, these files should use the `%s` syntax for string
  interpolation.
  \n`Args`: 
  \n\t filepath (str): The path to the file to read.
  \n\t args (tuple): The parameters to interpolate into the file.
  \n`Returns`: The contents of the file as a string.
  """
  try: 
    file_contents = ""
    with open(filepath, "r") as file:
      file_contents = file.read()

    params = ()
    if len(args) > 0:
      (params,) = args

    # Make sure file_contents isn't an empty string
    if file_contents == "":
      raise Exception("File is empty: %s" % filepath)
  except Exception as error:
    logging.error("Error while reading file: {}".format(filepath), error)
  
  try:
    query = file_contents.format(*params)
    database.execute(query)
    results = []
    if 'SELECT' in query or 'RETURNING' in query:
      results = database.fetchall()
    connection.commit()
    return results
  except (Exception, psycopg2.Error) as error:
    logging.error("Error while executing query: {}".format(query), error)
    connection.rollback() # I don't know if this is necessary

def migrate():
  """
  Select db_version from db_versions table
  Sort db_migrate files by number
  Run migrations that are greater than the current version
  """
  try:
    database.execute("SELECT db_version FROM db_versions ORDER BY db_version DESC LIMIT 1")
    ((db_version),) = database.fetchone()
    logging.info("Current database version: {}".format(db_version))

    # Run migrations
    migrations = os.listdir("db/db_migrate")
    migrations.sort()
    for migration in migrations:
      migration_number = int(migration.split(".")[0])
      if migration_number > db_version:
        print("Running migration: {}".format(migration))
        db_file("db/db_migrate/{}".format(migration))
        database.execute("INSERT INTO db_versions (db_version) VALUES ({})".format(migration_number))
        connection.commit()
        logging.info("Migration {} complete".format(migration_number))
  except (Exception, psycopg2.Error) as error:
    logging.error("Error while migrating the database", error)

def connect_to_db():
  """
  Connects to the database using the DATABASE_URL environment variable.
  """
  try:
    result = urlparse(os.getenv("DATABASE_URL"))
    username = result.username
    password = result.password
    dbname = result.path[1:]
    hostname = result.hostname

    connection_string = "dbname={} user={} password={} host={}".format(
      dbname, username, password, hostname
    )

    global connection
    connection = psycopg2.connect(connection_string)

    global database
    database = connection.cursor()

    logging.info("Connected to database...")

    migrate()
  except (Exception, psycopg2.Error) as error:
    logging.error("Error while connecting to database", error)

def close_db_connection():
  """
  Closes the database connection.
  """
  try:
    if connection:
      database.close()
      connection.close()
      logging.info("Database connection closed.")
  except (Exception, psycopg2.Error) as error:
    logging.error("Error while closing database connection", error)
