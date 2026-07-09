from neo4j import GraphDatabase
import pandas as pd

def setup_database_rules(session):
    session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (a:Airport) REQUIRE a.airport_id IS UNIQUE")
    session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (a:Airline) REQUIRE a.airline_id IS UNIQUE")
    session.run("CREATE INDEX IF NOT EXISTS FOR (a:Airport) ON (a.city)")

def ingest_airports(session, data_dir):
    airports = pd.read_csv(f'{data_dir}/airports_clean.csv', keep_default_na=False)

    query = """
    UNWIND $rows AS row
    MERGE (a:Airport {airport_id: toInteger(row.airport_id)})
    SET a.name = row.name, a.city = row.city, a.country = row.country, a.iata = row.iata
    """
    session.run(query, rows=airports.to_dict('records'))

def ingest_airlines(session, data_dir):
    airlines = pd.read_csv(f'{data_dir}/airlines_clean.csv', keep_default_na=False)
    
    query = """
    UNWIND $rows AS row
    MERGE (a:Airline {airline_id: toInteger(row.airline_id)})
    SET a.name = row.name, a.iata = row.iata, a.country = row.country
    """
    session.run(query, rows=airlines.to_dict('records'))

def ingest_routes(session, data_dir):
    routes = pd.read_csv(f'{data_dir}/routes_clean.csv', keep_default_na=False)
    
    query = """
    UNWIND $rows AS row
    MATCH (source:Airport {airport_id: toInteger(row.source_airport_id)})
    MATCH (dest:Airport {airport_id: toInteger(row.destination_airport_id)})
    MERGE (source)-[r:FLIES_TO {airline_id: toInteger(row.airline_id)}]->(dest)
    """
    session.run(query, rows=routes.to_dict('records'))

def main():
    data_dir = 'data'
    driver = GraphDatabase.driver("neo4j://127.0.0.1:7687", auth=("neo4j", "password"))
    
    with driver.session() as session:
        setup_database_rules(session)
        ingest_airports(session, data_dir)
        ingest_airlines(session, data_dir)
        ingest_routes(session, data_dir)
        
    driver.close()

if __name__ == "__main__":
    main()
