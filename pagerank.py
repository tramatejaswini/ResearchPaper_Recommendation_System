import driver
#ad articles and Autrs
query= """CALL apoc.periodic.iterate(
  'UNWIND ["dblp-ref-0.json","dblp-ref-1.json","dblp-ref-2.json","dblp-ref-3.json"] as file 
   CALL apoc.load.json("https://github.com/mneedham/link-prediction/raw/master/data/" + file) 
   yield value return value',
  'MERGE (a:Article{index:value.id}) 
   ON CREATE SET a += apoc.map.clean(value,["id","authors","references"],[0]) 
   WITH a,value.authors as authors 
   UNWIND authors as author 
   MERGE (b:Author{name:author}) 
   MERGE (b)-[:AUTHOR]->(a)'
,{batchSize: 10000, iterateList: true})"""

with driver.session() as session:
    session.run(query)

# oadng references
query1= """CALL apoc.periodic.iterate(
  'UNWIND ["dblp-ref-0.json","dblp-ref-1.json","dblp-ref-2.json","dblp-ref-3.json"] as file 
   CALL apoc.load.json("https://github.com/mneedham/link-prediction/raw/master/data/" + file) 
   yield value return value',
  'MERGE (a:Article{index:value.id}) 
   WITH a,value.references as references 
   UNWIND references as reference 
   MERGE (b:Article{index:reference}) 
   MERGE (a)-[:REFERENCES]->(b)'
,{batchSize: 10000, iterateList: true})"""

with driver.session() as session:
    session.run(query1)

# 
query2= """
CALL algo.pageRank('Article', 'REFERENCES')
MATCH (a:Article)
RETURN a.title as article,
       a.pagerank as score
ORDER BY score DESC 
LIMIT 10"""

with driver.session() as session:
    session.run(query2)
    
#indexing the Article and Absrac
query3= """
CALL db.index.fulltext.createNodeIndex('articlesAll', 
  ['Article'], ['title', 'abstract'])

CALL db.indexes()
CALL db.index.fulltext.awaitIndex("articlesAll")

:param searchTerm => '"social networks"'
CALL db.index.fulltext.queryNodes("articlesAll", $searchTerm)
YIELD node, score
RETURN count(*)"""

with driver.session() as session:
    session.run(query3)

# fnding similarfiles fnction 
query4 = """CALL db.index.fulltext.queryNodes("articlesAll", $searchTerm)
YIELD node, score
RETURN node.id, node.title,  score
LIMIT 10"""

with driver.session() as session:
    session.run(query4)

# sending results pagerank algorithm
query5 = """CALL db.index.fulltext.queryNodes("articlesAll", $searchTerm)
YIELD node
WITH collect(node) as articles
CALL algo.pageRank.stream('Article', 'REFERENCES', { 
  sourceNodes: articles 
})
YIELD nodeId, score
WITH nodeId,score 
ORDER BY score DESC 
LIMIT 10
RETURN algo.getNodeById(nodeId).title as article, score"""

with driver.session() as session:
    session.run(query5)

