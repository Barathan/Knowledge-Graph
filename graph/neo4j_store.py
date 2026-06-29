import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()


class Neo4jStore:

    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(
                os.getenv("NEO4J_USERNAME"),
                os.getenv("NEO4J_PASSWORD")
            )
        )

    def test_connection(self):
        with self.driver.session() as session:
            result = session.run(
                "RETURN 'Connected to Neo4j AuraDB!' AS message"
            )
            print(result.single()["message"])

    def close(self):
        self.driver.close()