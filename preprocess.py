import pandas as pd

def clean_airports(data_dir):
    airports_cols = ['airport_id', 'name', 'city', 'country', 'iata', 'icao', 'latitude', 'longitude', 'altitude', 'timezone', 'dst', 'tz', 'type', 'source']
    
    airports = pd.read_csv(f'{data_dir}/airports.dat', header=None, names=airports_cols, na_values=['\\N'])
    
    airports = airports.fillna("") 
    airports.to_csv(f'{data_dir}/airports_clean.csv', index=False)

def clean_airlines(data_dir):
    airlines_cols = ['airline_id', 'name', 'alias', 'iata', 'icao', 'callsign', 'country', 'active']
    airlines = pd.read_csv(f'{data_dir}/airlines.dat', header=None, names=airlines_cols, na_values=['\\N'])
    airlines = airlines.fillna("")
    airlines.to_csv(f'{data_dir}/airlines_clean.csv', index=False)

def clean_routes(data_dir):
    routes_cols = ['airline', 'airline_id', 'source_airport', 'source_airport_id', 'destination_airport', 'destination_airport_id', 'codeshare', 'stops', 'equipment']
    routes = pd.read_csv(f'{data_dir}/routes.dat', header=None, names=routes_cols, na_values=['\\N'])

    routes = routes.dropna(subset=['source_airport_id', 'destination_airport_id', 'airline_id'])

    routes['source_airport_id'] = routes['source_airport_id'].astype(int)
    routes['destination_airport_id'] = routes['destination_airport_id'].astype(int)
    routes['airline_id'] = routes['airline_id'].astype(int)

    routes = routes.fillna("")
    routes.to_csv(f'{data_dir}/routes_clean.csv', index=False)

def main():
    data_dir = 'data'
    clean_airports(data_dir)
    clean_airlines(data_dir)
    clean_routes(data_dir)

if __name__ == "__main__":
    main()
