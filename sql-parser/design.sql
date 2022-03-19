CREATE DATABASE wikilinks;
USE wikilinks;

CREATE TABLE Page (
  id INT NOT NULL AUTO_INCREMENT,
  title VARBINARY(255) NOT NULL UNIQUE,

  PRIMARY KEY (id)
);


CREATE TABLE Link (
  src INT,
  dest INT,
  redirect BOOLEAN DEFAULT false,
  FOREIGN KEY (src) REFERENCES Page(id),
  FOREIGN KEY (dest) REFERENCES Page(id),
  PRIMARY KEY (src,dest)
);


CREATE USER 'wiki'@'%' identified by 'L1nKz';
GRANT SELECT,INSERT,UPDATE,DELETE on wikilinks.* TO 'wiki'@'%';
