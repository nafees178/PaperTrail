from neo4j import GraphDatabase

def setup_gds_graph(session):
    try:
        session.run("CALL gds.graph.drop('my_flight_graph') YIELD graphName").consume()
    except:
        pass

    session.run("""
    CALL gds.graph.project(
      'my_flight_graph',
      'Airport',
      'FLIES_TO'
    )
    """)

def run_pagerank(session):
    print("\n---Finding Most Imp Airport ---")
    result = session.run("""
    CALL gds.pageRank.stream('my_flight_graph')
    YIELD nodeId, score
    RETURN gds.util.asNode(nodeId).city AS City, score
    ORDER BY score DESC
    LIMIT 5
    """)
    for record in result:
        print(record.data())

def run_louvain(session):
    print("\n---(Finding regional groups/clusters) ---")
    result = session.run("""
    CALL gds.louvain.stream('my_flight_graph')
    YIELD nodeId, communityId
    RETURN communityId, count(nodeId) AS number_of_airports_in_group
    ORDER BY number_of_airports_in_group DESC
    LIMIT 5
    """)
    for record in result:
        print(record.data())

def cleanup(session):
    try:
        session.run("CALL gds.graph.drop('my_flight_graph') YIELD graphName").consume()
    except:
        pass

def main():
    driver = GraphDatabase.driver("neo4j://127.0.0.1:7687", auth=("neo4j", "password"))
    with driver.session() as session:
        setup_gds_graph(session)
        run_pagerank(session)
        run_louvain(session)
        cleanup(session)
    driver.close()

if __name__ == "__main__":
    main()
