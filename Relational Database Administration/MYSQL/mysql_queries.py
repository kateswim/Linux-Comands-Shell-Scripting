import mysql.connector
from mysql.connector import Error

# ---------- Connection settings ----------
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",  # No password for local MySQL (as installed by Homebrew)
    "database": "world"  # World database
}

def get_connection():
    """Get MySQL database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# ---------- Query functions ----------

def get_city_count():
    """Get total number of cities"""
    sql = "SELECT COUNT(*) FROM city;"
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            count = cursor.fetchone()[0]
            print(f"Total cities: {count:,}")
            return count
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

def get_country_count():
    """Get total number of countries"""
    sql = "SELECT COUNT(*) FROM country;"
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            count = cursor.fetchone()[0]
            print(f"Total countries: {count:,}")
            return count
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

def get_languages_count():
    """Get total number of languages"""
    sql = "SELECT COUNT(*) FROM countrylanguage;"
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            count = cursor.fetchone()[0]
            print(f"Total languages: {count:,}")
            return count
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

def get_cities_by_country(country_code, limit=10):
    """Get cities in a specific country"""
    sql = """
    SELECT Name, District, Population
    FROM city
    WHERE CountryCode = %s
    ORDER BY Population DESC
    LIMIT %s;
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (country_code, limit))
            rows = cursor.fetchall()
            print(f"\nCities in {country_code} (showing {len(rows)}):")
            for row in rows:
                print(f"  {row[0]} | {row[1]} | Population: {row[2]:,}")
            return rows
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

def get_countries_by_continent(continent, limit=10):
    """Get countries in a specific continent"""
    sql = """
    SELECT Code, Name, Population, SurfaceArea, LifeExpectancy
    FROM country
    WHERE Continent = %s
    ORDER BY Population DESC
    LIMIT %s;
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (continent, limit))
            rows = cursor.fetchall()
            print(f"\nCountries in {continent} (showing {len(rows)}):")
            for row in rows:
                print(f"  {row[0]} | {row[1]} | Pop: {row[2]:,} | Area: {row[3]:,.2f} km² | Life: {row[4]} years")
            return rows
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

def get_languages_by_country(country_code, limit=10):
    """Get languages spoken in a specific country"""
    sql = """
    SELECT Language, IsOfficial, Percentage
    FROM countrylanguage
    WHERE CountryCode = %s
    ORDER BY Percentage DESC
    LIMIT %s;
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (country_code, limit))
            rows = cursor.fetchall()
            print(f"\nLanguages in {country_code} (showing {len(rows)}):")
            for row in rows:
                official = "Official" if row[1] == 'T' else "Not Official"
                print(f"  {row[0]} | {official} | {row[2]}%")
            return rows
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

def get_top_cities_by_population(limit=10):
    """Get top cities by population"""
    sql = """
    SELECT Name, CountryCode, District, Population
    FROM city
    ORDER BY Population DESC
    LIMIT %s;
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (limit,))
            rows = cursor.fetchall()
            print(f"\nTop {limit} cities by population:")
            for row in rows:
                print(f"  {row[0]} ({row[1]}) | {row[2]} | {row[3]:,}")
            return rows
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

def get_country_info(country_code):
    """Get detailed information about a country"""
    sql = """
    SELECT Code, Name, Continent, Region, Population, SurfaceArea, 
           LifeExpectancy, GovernmentForm, HeadOfState
    FROM country
    WHERE Code = %s;
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (country_code,))
            row = cursor.fetchone()
            if row:
                print(f"\nCountry Information: {row[1]} ({row[0]})")
                print(f"  Continent: {row[2]}")
                print(f"  Region: {row[3]}")
                print(f"  Population: {row[4]:,}")
                print(f"  Surface Area: {row[5]:,.2f} km²")
                print(f"  Life Expectancy: {row[6]} years")
                print(f"  Government: {row[7]}")
                print(f"  Head of State: {row[8]}")
                return row
            else:
                print(f"Country {country_code} not found")
                return None
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("World Database Queries (MySQL)")
    print("=" * 60)
    
    # Get statistics
    get_city_count()
    get_country_count()
    get_languages_count()
    
    # Get top cities
    get_top_cities_by_population(limit=10)
    
    # Get countries by continent
    get_countries_by_continent("Europe", limit=5)
    
    # Get cities in a specific country (USA)
    get_cities_by_country("USA", limit=5)
    
    # Get languages in a specific country (USA)
    get_languages_by_country("USA", limit=5)
    
    # Get country info
    get_country_info("USA")
    
    print("\n" + "=" * 60)
    print("Query completed!")
    print("=" * 60)

