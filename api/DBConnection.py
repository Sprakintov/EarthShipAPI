import psycopg2

def connect_to_database(host, database, user, password, port="5432"):
    """
    Create a connection to PostgreSQL database
    """
    try:
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        print("Successfully connected to the database")
        return connection
    except Error as e:
        print(f"Error connecting to PostgreSQL: {str(e)}")
        return None
    

def query(sql):
    conn = connect_to_database("localhost", "EarthShip", "postgres", "spra")
    if conn is not None:
        cursor = conn.cursor() 
        # sql = """select "OrderID" from "public"."Base_order";"""
        cursor.execute(sql)
        res = cursor.fetchall()
        for order in res:
            print(order)
        cursor.close()
        conn.close()
    else:
        print("Failed to create a database connection.")