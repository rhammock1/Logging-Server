INSERT INTO messages (message, project)
VALUES ('{}', '{}')
RETURNING message_id;