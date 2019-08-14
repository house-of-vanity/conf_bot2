BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "heroes" (
	"name"	TEXT NOT NULL,
	PRIMARY KEY("name")
);
CREATE TABLE IF NOT EXISTS "patches" (
	"version"	TEXT NOT NULL,
	"release_date"	DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("version")
);
CREATE TABLE IF NOT EXISTS "hero_changes" (
	"type"	TEXT NOT NULL,
  "patch" INT NOT NULL,
  "hero" INT NOT NULL,
	"info"	TEXT NOT NULL,
	"meta"	TEXT,
	PRIMARY KEY("hero", "patch", "info")
);
COMMIT;
