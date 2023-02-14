import logging
from db import db_file

def save_message(message, project_id):
  """
  Saves a message to the database.
  """
  try:
    result = db_file("db/messages/insert.sql", (message, project_id,))
    if result is None:
      logging.error("Insert message failed")
      return
    logging.info("Records inserted successfully into messages table")
  except Exception as error:
    logging.error("Error while saving message", error)


def get_messages():
  """
  Gets all messages from the database.
  """
  try:
    result = db_file("db/messages/get.sql")
    if result is None:
      logging.error("Get messages failed")
      return
    logging.info("Successfully retrieved messages")
    return result
  except Exception as error:
    logging.error("Error while getting message", error)
