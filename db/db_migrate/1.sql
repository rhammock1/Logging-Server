CREATE TABLE messages (
  message TEXT NOT NULL,
  project TEXT NOT NULL,
  created TIMESTAMPTZ DEFAULT NOW()
);