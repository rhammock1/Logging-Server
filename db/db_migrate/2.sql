ALTER TABLE messages DROP COLUMN project;

ALTER TABLE messages ADD COLUMN project_id BIGINT REFERENCES projects(project_id);