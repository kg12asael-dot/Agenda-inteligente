from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            "bolt://localhost:7687",
            auth=("neo4j", "12345678")
        )

    def close(self):
        self.driver.close()

    def query(self, query, params=None):
        with self.driver.session(database="agenda-db") as session:
            result = session.run(query, params)
            return [record.data() for record in result]


db = Neo4jConnection()

