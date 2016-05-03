DROP DATABASE IF EXISTS projdb;
CREATE DATABASE projdb;
USE projdb;

CREATE TABLE `Users`(
	`id` MEDIUMINT(11) NOT NULL AUTO_INCREMENT,
	`username` VARCHAR (25),
    `email` VARCHAR (25) NOT NULL,

	`about` TEXT,
	`name` VARCHAR (25),
	`isAnonymous` BOOL NOT NULL DEFAULT False,

	PRIMARY KEY (`id`),
    UNIQUE KEY USING HASH (`email`),
    KEY USING HASH (`name`)
) ENGINE = MYISAM;


CREATE TABLE `Forums`(
	`id` MEDIUMINT(11) NOT NULL AUTO_INCREMENT,
    `short_name` VARCHAR (35) NOT NULL,
    `user` VARCHAR (25) NOT NULL,
	`name` VARCHAR (35) NOT NULL,

	PRIMARY KEY (`id`),
    UNIQUE KEY USING HASH (`short_name`),
    UNIQUE KEY USING HASH (`name`),
    KEY USING HASH (`user`),
    CONSTRAINT FOREIGN KEY (`user`) REFERENCES `Users` (`email`) ON DELETE CASCADE
) ENGINE = MYISAM;


CREATE TABLE `Threads` (
    `id` MEDIUMINT(11) NOT NULL AUTO_INCREMENT,
    `forum` VARCHAR (35) NOT NULL,
    `user` VARCHAR (25) NOT NULL,

    `title` VARCHAR (50) NOT NULL,
    `date` DATETIME NOT NULL,
    `message` TEXT NOT NULL,
    `slug` VARCHAR (50) NOT NULL,

    `isDeleted` BOOL NOT NULL DEFAULT False,
    `isClosed` BOOL NOT NULL DEFAULT False,
    `dislikes` SMALLINT NOT NULL DEFAULT 0,
    `likes` SMALLINT NOT NULL DEFAULT 0,
    `points` SMALLINT NOT NULL DEFAULT 0,
    `posts` SMALLINT NOT NULL DEFAULT 0,

    PRIMARY KEY (`id`),
    KEY USING HASH (`slug`),
    KEY USING HASH (`forum`),
    CONSTRAINT FOREIGN KEY (`forum`) REFERENCES `Forums` (`short_name`) ON DELETE CASCADE,
    CONSTRAINT FOREIGN KEY (`user`) REFERENCES `Users` (`email`) ON DELETE CASCADE
) ENGINE = MYISAM;

ALTER TABLE `Threads` ADD INDEX idx_thread_ud (`user`, `date`);

CREATE TABLE `Posts` (
	`id` MEDIUMINT(11) NOT NULL AUTO_INCREMENT,
    `thread` MEDIUMINT(11) NOT NULL,
    `user` VARCHAR (25) NOT NULL,
    `forum` VARCHAR (35) NOT NULL,

    `date` DATETIME NOT NULL,
    `message` TEXT NOT NULL,
    `dislikes` SMALLINT NOT NULL DEFAULT 0,
    `likes` SMALLINT NOT NULL DEFAULT 0,
    `points` SMALLINT NOT NULL DEFAULT 0,

	`parent` MEDIUMINT(11),
	`path` VARCHAR(113) NOT NULL DEFAULT '',
	`isHighlighted` BOOL NOT NULL DEFAULT False,
	`isApproved` BOOL NOT NULL DEFAULT False,
	`isEdited` BOOL NOT NULL DEFAULT False,
	`isSpam` BOOL NOT NULL DEFAULT False,
	`isDeleted` BOOL NOT NULL DEFAULT False,

	PRIMARY KEY (`id`),
    KEY (`parent`),
    CONSTRAINT FOREIGN KEY (`forum`) REFERENCES `Forums` (`short_name`) ON DELETE CASCADE,
    CONSTRAINT FOREIGN KEY (`user`) REFERENCES `Users` (`email`) ON DELETE CASCADE,
    CONSTRAINT FOREIGN KEY (`thread`) REFERENCES `Threads` (`id`) ON DELETE CASCADE
) ENGINE = MYISAM;


ALTER TABLE `Posts` ADD INDEX idx_post_fu (`forum`, `user`);
ALTER TABLE `Posts` ADD INDEX idx_post_fd (`forum`, `date`);
ALTER TABLE `Posts` ADD INDEX idx_post_td (`thread`, `date`);
ALTER TABLE `Posts` ADD INDEX idx_post_ud (`user`, `date`);


DROP TRIGGER IF EXISTS ins_post;
CREATE TRIGGER ins_post
BEFORE INSERT ON `Posts`
FOR EACH ROW
UPDATE `Threads` SET `posts` = `posts` + 1 WHERE `id` = NEW.`thread`;

DROP TRIGGER IF EXISTS del_post;

CREATE TABLE `Follow` (
    `id` MEDIUMINT(11) NOT NULL AUTO_INCREMENT,
    `follower` VARCHAR (25) NOT NULL,
    `followee` VARCHAR (25) NOT NULL,

    PRIMARY KEY (`id`),
    KEY USING HASH (`follower`),
    CONSTRAINT FOREIGN KEY (`follower`) REFERENCES `Users` (`email`) ON DELETE CASCADE,
    KEY USING HASH (`followee`),
    CONSTRAINT FOREIGN KEY (`followee`) REFERENCES `Users` (`email`) ON DELETE CASCADE
) ENGINE = MYISAM;

CREATE TABLE `Subscribe` (
    `id` MEDIUMINT(11) NOT NULL AUTO_INCREMENT,
    `user` CHAR (25) NOT NULL,
    `thread` MEDIUMINT(11) NOT NULL,

    PRIMARY KEY (`id`),
    KEY USING HASH (`user`),
    CONSTRAINT FOREIGN KEY (`user`) REFERENCES `Users` (`email`) ON DELETE CASCADE,
    KEY (`thread`),
    CONSTRAINT FOREIGN KEY (`thread`) REFERENCES `Threads` (`id`) ON DELETE CASCADE
) ENGINE = MYISAM;