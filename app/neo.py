from neo4j import GraphDatabase
import os

import dependencies
import models

NEO4J_URI = "bolt://neo4j:7687"
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "your_password")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def start_up():
    mydb = next(dependencies.get_mysql_db())
    with driver.session() as session:
        usuarios = mydb.query(models.Usuario).all()
        for user in usuarios:
            session.run("""
                MERGE (u:Usuario {id: $id, nombre: $nombre });
            """, id=user.id, nombre=user.nombre)
        empresas = mydb.query(models.Empresa).all()
        for empresa in empresas:
            session.run("""
                MERGE (e:Empresa {id: $id, nombre: $nombre });
            """, id=empresa.id, nombre=empresa.nombre)
        print("✅ Neo4j nodes created")
        connections = [
            """MATCH (a:Usuario {id: 1}), (b:Usuario {id: 2}) MERGE (a)-[:CONNECTED_TO]->(b);""",
            """MATCH (a:Usuario {id: 1}), (b:Usuario {id: 3}) MERGE (a)-[:CONNECTED_TO]->(b);""",
            """MATCH (a:Usuario {id: 1}), (b:Usuario {id: 4}) MERGE (a)-[:CONNECTED_TO]->(b);""",
            """MATCH (a:Usuario {id: 1}), (b:Usuario {id: 10}) MERGE (a)-[:CONNECTED_TO]->(b);""",
            """MATCH (a:Usuario {id: 3}), (b:Usuario {id: 2}) MERGE (a)-[:CONNECTED_TO]->(b);""",
            """MATCH (a:Usuario {id: 3}), (b:Usuario {id: 4}) MERGE (a)-[:CONNECTED_TO]->(b);""",
            """MATCH (a:Usuario {id: 3}), (b:Usuario {id: 7}) MERGE (a)-[:CONNECTED_TO]->(b);""",
            """MATCH (a:Usuario {id: 3}), (b:Usuario {id: 9}) MERGE (a)-[:CONNECTED_TO]->(b);""",
            """MATCH (a:Usuario {id: 4}), (b:Usuario {id: 7}) MERGE (a)-[:CONNECTED_TO]->(b);""",
            """MATCH (a:Usuario {id: 6}), (b:Usuario {id: 8}) MERGE (a)-[:CONNECTED_TO]->(b);""",
            """MATCH (a:Usuario {id: 7}), (b:Usuario {id: 9}) MERGE (a)-[:CONNECTED_TO]->(b);""",
            """MATCH (a:Usuario {id: 8}), (b:Usuario {id: 10}) MERGE (a)-[:CONNECTED_TO]->(b);""",
            """MATCH (a:Usuario {id: 9}), (b:Usuario {id: 1}) MERGE (a)-[:CONNECTED_TO]->(b);""",
        ]
        for connection in connections:
            session.run(connection)
        recomendations = [
            """MATCH (e:Empresa {id: 1}), (u:Usuario {id: 2}) MERGE (e)-[:RECOMMENDED]->(u);""",
            """MATCH (e:Empresa {id: 2}), (u:Usuario {id: 3}) MERGE (e)-[:RECOMMENDED]->(u);""",
            """MATCH (e:Empresa {id: 1}), (u:Usuario {id: 5}) MERGE (e)-[:RECOMMENDED]->(u);""",
            """MATCH (e:Empresa {id: 3}), (u:Usuario {id: 2}) MERGE (e)-[:RECOMMENDED]->(u);""",
            """MATCH (e:Empresa {id: 9}), (u:Usuario {id: 2}) MERGE (e)-[:RECOMMENDED]->(u);""",
            """MATCH (e:Empresa {id: 4}), (u:Usuario {id: 1}) MERGE (e)-[:RECOMMENDED]->(u);""",
            """MATCH (e:Empresa {id: 7}), (u:Usuario {id: 1}) MERGE (e)-[:RECOMMENDED]->(u);"""
        ]
        for recomendation in recomendations:
            session.run(recomendation)
        print("✅ Neo4j constraints created")