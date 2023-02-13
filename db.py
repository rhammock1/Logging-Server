from dotenv import load_dotenv
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

    (params,) = args

    # Make sure file_contents isn't an empty string
    if file_contents == "":
      raise Exception("File is empty: %s" % filepath)
  except Exception as error:
    logging.error("Error while reading file: %s", filepath, error)
  
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

def connect_to_db():
  try:
    connection_string = "dbname=%s user=%s" % (
      os.getenv("DATABASE_NAME"), os.getenv("DATABASE_USER"))

    global connection
    connection = psycopg2.connect(connection_string)

    global database
    database = connection.cursor()

    logging.info("Connected to database...")
  except (Exception, psycopg2.Error) as error:
    logging.error("Error while connecting to database", error)

def close_db_connection():
  try:
    if connection:
      database.close()
      connection.close()
      logging.info("Database connection closed.")
  except (Exception, psycopg2.Error) as error:
    logging.error("Error while closing database connection", error)
