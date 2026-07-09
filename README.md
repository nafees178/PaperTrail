# OpenFlights Graph Database Analysis

This project ingests and analyzes the OpenFlights dataset using a Neo4j Graph Database. The pipeline consists of data preprocessing, graph ingestion, Cypher querying, and Graph Data Science (GDS) algorithm execution.

## 1. Schema Decisions & Graph Data Model

The data is modeled to optimize for routing and network analysis between airports:

- **Nodes:**
  - `Airport`: Represents a physical airport location. Key properties include `airport_id`, `name`, `city`, `country`, and `iata`.
  - `Airline`: Represents an airline company. Key properties include `airline_id`, `name`, `iata`, and `country`.
- **Relationships:**
  - `(Airport)-[FLIES_TO]->(Airport)`: Represents a directed flight route between two airports. 
  - **Decision:** Instead of creating a complex path involving the `Airline` node (e.g., `(Airport)<-[:DEPARTS]-(Flight)-[:ARRIVES]->(Airport)`), the `airline_id` is stored directly as a property on the `FLIES_TO` relationship. This heavily optimizes graph traversals (like finding the shortest path between two cities) by reducing the number of hops required in the query while still retaining which airline operates the route.
- **Constraints & Indexes:**
  - Unique constraints are enforced on `Airport.airport_id` and `Airline.airline_id` to guarantee referential integrity and prevent duplicate entity creation during ingestion.
  - An index is applied to `Airport.city` to accelerate text-based lookup queries.

## 2. Cypher Queries

The `queries.py` script executes several fundamental graph operations:

1. **Node Lookup:** Exact matching for an airport by its IATA code (`JFK`), demonstrating basic node retrieval.
2. **Property Filtering:** Finding airlines based in a specific country (`United Kingdom`).
3. **Aggregation:** Calculating the top 5 airports with the highest out-degree (most outgoing `FLIES_TO` relationships).
4. **Variable-Length Paths:** Discovering 1-stop layover routes between `New York` and `London`.
5. **Shortest Path:** Utilizing Neo4j's built-in `shortestPath()` algorithm to find the minimum number of flights required to travel between `Sydney` and `London`.

## 3. Algorithm Results & Insights

The `gds_analysis.py` script projects the graph into memory and runs two primary Graph Data Science (GDS) algorithms: PageRank and Louvain Community Detection.

### Concrete Insights

1. **The Hub-and-Spoke Model (PageRank Insight):** 
   PageRank measures transitive influence within the network. The results consistently highlight major international airports (e.g., Atlanta, Heathrow, Dubai) possessing disproportionately high PageRank scores. This confirms that the global aviation network operates on a "hub-and-spoke" model, relying heavily on a few massive central nodes to route global traffic rather than utilizing a decentralized, point-to-point architecture.

2. **Geographic Network Modularity (Louvain Insight):**
   The Louvain algorithm detects communities based on edge density. When applied to the OpenFlights dataset, the algorithm naturally partitions the global graph into distinct, isolated clusters that heavily correlate with geographic continents (e.g., North America, Europe, Asia). The insight here is that the vast majority of global flights are intra-regional. Inter-continental flights exist primarily as sparse "bridge" connections linking the distinct, dense regional communities together.

---

## 4. How to Rebuild the Project

You can rebuild this entire project from the raw `.dat` files without any manual database edits or UI interactions (other than starting the DBMS).

### Prerequisites
1. **Neo4j Desktop:** Installed and running.
2. **GDS Plugin:** You must install the **Graph Data Science (GDS)** plugin on your database via the Neo4j Desktop interface before starting it.
3. **Database Credentials:** The default scripts expect a local database with the username `neo4j` and password `password`. Update the `auth=` parameter in the scripts if your credentials differ.
4. **Python Dependencies:** Install the required packages via terminal:
   ```bash
   pip install pandas neo4j
   ```

### Execution Steps
Ensure the raw OpenFlights datasets (`airports.dat`, `airlines.dat`, `routes.dat`) are placed inside the `data/` directory. Then, run the scripts in the following order:

1. **Clean the Data:**
   ```bash
   python preprocess.py
   ```
   *This reads the raw `.dat` files, handles missing values, ensures integer types for IDs, and outputs clean `.csv` files.*

2. **Ingest the Graph:**
   ```bash
   python ingest.py
   ```
   *This connects to your running Neo4j instance, establishes constraints/indexes, and batches the `.csv` data into Nodes and Relationships using Cypher `UNWIND`.*

3. **Run Queries:**
   ```bash
   python queries.py
   ```
   *This executes the standard Cypher queries against the newly built database.*

4. **Run GDS Analysis:**
   ```bash
   python gds_analysis.py
   ```
   *This projects the graph into memory and executes the PageRank and Louvain algorithms to generate insights.*
