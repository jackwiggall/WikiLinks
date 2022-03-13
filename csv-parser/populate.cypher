
!!! files need to be inside /var/lib/neo4j/import, thats where file:/// root is!!
CREATE CONSTRAINT ON (p:Page) ASSERT p.title IS UNIQUE;
USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM 'file:///titles.csv' AS line
MERGE (:Page{title: line.title});
!! merge is like create except wont overwrite on duplicate


USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS line
MATCH (src:Page), (dest:Page)
WHERE src.title = line.src AND dest.title = line.dest
CREATE (src)-[:LINKS]->(dest);


#USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS line
#MATCH (src:Page {title:line.src}), (dest:Page {title:line.dest})
#CREATE (src)-[:LINKS]->(dest);


MATCH (src:Page), (dest:Page)
WHERE src.title = 'Anarchism' AND dest.title = 'AfghanistanGeography'
CREATE (src)-[r:LINKS]->(dest)
RETURN type(r)


! delete all pages
MATCH (p:Page)
WITH p limit 1000000 // heap error without this
DETACH DELETE p


! populate 
USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS row
MERGE (src:Page { title: row.src })
MERGE (dest:Page { title: row.dest })
MERGE (src)-[:LINKS]->(dest)