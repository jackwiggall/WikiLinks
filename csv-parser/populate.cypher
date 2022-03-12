!!! files need to be inside /var/lib/neo4j/import, thats where file:/// root is!!
USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM 'file:///titles.csv' AS line
CREATE (:Page{title: line.title});

USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS line
MATCH (src:Page), (dest:Page)
WHERE src.title = line.src AND dest.title = line.dest
CREATE (src)-[:LINKS]->(dest);


USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS line
MATCH (src:Page {title:line.src}), (dest:Page {title:line.dest})
CREATE (src)-[:LINKS]->(dest);

