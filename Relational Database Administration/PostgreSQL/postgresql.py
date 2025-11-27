import psycopg2
from psycopg2 import Error

# ---------- Connection settings ----------
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "demo",      # flights database
    "user": "katehoncharova",    # your PostgreSQL username
    "password": ""  # No password needed for local PostgreSQL
}

def get_connection():
    """Get PostgreSQL database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

# ---------- Query flights data ----------
def get_flight_count():
    """Get total number of flights"""
    sql = "SELECT COUNT(*) FROM bookings.flights;"
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(sql)
                count = cur.fetchone()[0]
            print(f"Total flights: {count}")
            return count
        except Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            conn.close()
    return None

# ---------- Get flights by route ----------
def get_flights_by_route(departure_airport, arrival_airport, limit=10):
    """Get flights between two airports"""
    sql = """
    SELECT flight_no, scheduled_departure, scheduled_arrival, status
    FROM bookings.flights
    WHERE departure_airport = %s AND arrival_airport = %s
    ORDER BY scheduled_departure
    LIMIT %s;
    """
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (departure_airport, arrival_airport, limit))
                rows = cur.fetchall()
            print(f"\nFlights from {departure_airport} to {arrival_airport}:")
            for row in rows:
                print(f"  {row[0]} | {row[1]} | {row[2]} | {row[3]}")
            return rows
        except Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            conn.close()
    return None

# ---------- Get airports ----------
def list_airports(limit=20):
    """List airports"""
    sql = """
    SELECT airport_code, airport_name, city
    FROM bookings.airports_data
    ORDER BY city
    LIMIT %s;
    """
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (limit,))
                rows = cur.fetchall()
            print(f"\nAirports (showing {len(rows)}):")
            for row in rows:
                print(f"  {row[0]} | {row[1]} | {row[2]}")
            return rows
        except Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            conn.close()
    return None

# ---------- Get bookings count ----------
def get_bookings_count():
    """Get total number of bookings"""
    sql = "SELECT COUNT(*) FROM bookings.bookings;"
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(sql)
                count = cur.fetchone()[0]
            print(f"Total bookings: {count:,}")
            return count
        except Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            conn.close()
    return None

# ---------- Get recent flights ----------
def get_recent_flights(limit=10):
    """Get recent flights"""
    sql = """
    SELECT flight_no, departure_airport, arrival_airport, 
           scheduled_departure, scheduled_arrival, status
    FROM bookings.flights
    ORDER BY scheduled_departure DESC
    LIMIT %s;
    """
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (limit,))
                rows = cur.fetchall()
            print(f"\nRecent flights (showing {len(rows)}):")
            for row in rows:
                print(f"  {row[0]} | {row[1]} → {row[2]} | {row[3]} | {row[4]} | {row[5]}")
            return rows
        except Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            conn.close()
    return None

if __name__ == "__main__":
    print("=" * 60)
    print("Flights Database Queries")
    print("=" * 60)
    
    # Get statistics
    get_flight_count()
    get_bookings_count()
    
    # List some airports
    list_airports(limit=10)
    
    # Get recent flights
    get_recent_flights(limit=5)
    
    # Example: Get flights from Moscow to St. Petersburg
    get_flights_by_route("DME", "LED", limit=5)
    
    print("\n" + "=" * 60)
    print("Query completed!")
    print("=" * 60)
