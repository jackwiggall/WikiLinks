CREATE DATABASE wikilinks;
USE wikilinks;

CREATE TABLE Page (
  id INT NOT NULL AUTO_INCREMENT,
  title NVARCHAR(255) NOT NULL UNIQUE,
  title_upper NVARCHAR(255) NULL,

  redirect NVARCHAR(255) NULL,


  content MEDIUMBLOB NULL,
  PRIMARY KEY (id)
);


CREATE TABLE Link (
  src INT,
  dest INT,
  FOREIGN KEY (src) REFERENCES Page(id),
  FOREIGN KEY (dest) REFERENCES Page(id),
  PRIMARY KEY (src,dest)
);

CREATE USER wiki@localhost identified by 'L1nKz';
GRANT SELECT,INSERT,UPDATE,DELETE on wikilinks.* TO wiki@localhost;



---

INSERT INTO Link (src,dest)
  (SELECT (SELECT id FROM Page WHERE title="src"),
    id FROM Page WHERE title="dest");
