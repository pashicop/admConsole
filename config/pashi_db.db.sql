BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Users_in_Groups" (
	"id"	INTEGER NOT NULL UNIQUE,
	"user_id"	INTEGER NOT NULL,
	"group_id"	INTEGER NOT NULL,
	"is_boss"	INTEGER DEFAULT 0,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("group_id") REFERENCES "Groups"("id"),
	FOREIGN KEY("user_id") REFERENCES "Users"("id")
);
CREATE TABLE IF NOT EXISTS "Users" (
	"id"	TEXT NOT NULL UNIQUE,
	"Login"	TEXT NOT NULL UNIQUE,
	"Password"	TEXT NOT NULL DEFAULT 'qwerty',
	"Display_name"	TEXT NOT NULL,
	"is_dispatcher"	INTEGER DEFAULT 0,
	"is_admin"	INTEGER DEFAULT 0,
	"is_blocked"	INTEGER DEFAULT 0,
	"is_gw"	INTEGER DEFAULT 0,
	"previous_type"	INTEGER DEFAULT 0,
	"en_ind"	INTEGER DEFAULT 1,
	"en_del_chats" INTEGER DEFAULT 0,
	"en_partial_drop" INTEGER DEFAULT 0,
	"priority" INTEGER DEFAULT 1,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "Groups" (
	"id"	TEXT NOT NULL UNIQUE,
	"Name"	TEXT NOT NULL UNIQUE,
	"description"	TEXT DEFAULT NULL,
	"priority"	INTEGER DEFAULT 0,
	"is_broadcast"	INTEGER DEFAULT 0,
	"is_emergency"	INTEGER DEFAULT 0,
	"is_disabled"	INTEGER DEFAULT 0,
	PRIMARY KEY("id")
);
COMMIT;
