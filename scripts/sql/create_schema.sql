

CREATE TABLE user (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  userid    TEXT NOT NULL,
  passwd    TEXT NOT NULL,
  active    INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE role (
  id        TEXT NOT NULL PRIMARY KEY,
  name      TEXT NOT NULL
);

CREATE TABLE UserRoleAssoc (
  user_id   INTEGER NOT NULL,
  role_id   TEXT NOT NULL,
  PRIMARY KEY (user_id, role_id),
  FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE,
  FOREIGN KEY (role_id) REFERENCES role (id) ON DELETE CASCADE
);

CREATE TABLE device (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  name      TEXT NOT NULL,
  address   INTEGER NOT NULL,
  type_id   INTEGER NOT NULL
);

CREATE TABLE type (
  id        INTEGER NOT NULL PRIMARY KEY,
  name      TEXT NOT NULL,
  driver    TEXT NOT NULL
);

