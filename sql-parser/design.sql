CREATE DATABASE wikilinks;
USE wikilinks;

CREATE TABLE Page (
  id INT NOT NULL AUTO_INCREMENT,
  title VARBINARY (255) NOT NULL UNIQUE,
  
  redirect VARCHAR(255) NULL,

  content MEDIUMBLOB NULL,
  PRIMARY KEY (id)
);


CREATE TABLE Link (
  src INT,
  dest INT,
  FOREIGN KEY (src) REFERENCES Page(id),
  FOREIGN KEY (dest) REFERENCES Page(id)
);

CREATE USER wiki@localhost identified by 'L1nKz';
GRANT SELECT,INSERT,UPDATE,DELETE on wikilinks.* TO wiki@localhost;