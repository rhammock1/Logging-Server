CREATE TABLE messages (
  message_id BIGSERIAL PRIMARY KEY,
  message TEXT NOT NULL,
  project TEXT NOT NULL,
  created TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE projects (
  project_id BIGSERIAL PRIMARY KEY,
  project TEXT NOT NULL,
  created TIMESTAMPTZ DEFAULT NOW()
);