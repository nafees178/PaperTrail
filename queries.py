from neo4j import GraphDatabase

def run_simple_lookup(session):
    result = session.run("MATCH (a:Airport {iata: 'JFK'}) RETURN a.name, a.city, a.country")
    for record in result:
        print(record.data())

def run_filtering_query(session):
    result = session.run("MATCH (al:Airline {country: 'United Kingdom'}) RETURN al.name LIMIT 5")
    for record in result:
        print(record.data())

def run_aggregation_query(session):
    query = """
    MATCH (source:Airport)-[r:FLIES_TO]->(dest:Airport)
    RETURN source.city AS City, count(r) AS Total_Flights
    ORDER BY Total_Flights DESC
    LIMIT 5
    """
    result = session.run(query)
    for record in result:
        print(record.data())

def run_path_query(session):
    query = """
    MATCH path = (start:Airport {city: 'New York'})-[:FLIES_TO]->(layover:Airport)-[:FLIES_TO]->(end:Airport {city: 'London'})
    RETURN layover.name AS Layover_Airport
    LIMIT 5
    """
    result = session.run(query)
    for record in result:
        print(record.data())

def run_shortest_path_query(session):
    query = """
    MATCH path = shortestPath((start:Airport {city: 'Sydney'})-[:FLIES_TO*..5]->(end:Airport {city: 'London'}))
    RETURN length(path) AS Number_of_Flights_Needed
    """
    result = session.run(query)
    for record in result:
        print(record.data())

def main():
    driver = GraphDatabase.driver("neo4j://127.0.0.1:7687", auth=("neo4j", "password"))
    with driver.session() as session:
        run_simple_lookup(session)
        run_filtering_query(session)
        run_aggregation_query(session)
        run_path_query(session)
        run_shortest_path_query(session)
    driver.close()

if __name__ == "__main__":
    main()
