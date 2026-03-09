"""this script gets the MySQL session and defines all the tables and relations
database name = aa_project, table name = user_details, user_amenities"""
import mysql.connector


def get_con():
    try:
        con = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "password",
            database = "aa_project"
        )
        return con
    except Exception as e:
        return f"error in mysql connection: {e}"


def create_db():
    con = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password"
    )

    cursor = con.cursor()
    query = "CREATE DATABASE IF NOT EXISTS aa_project"
    cursor.execute(query)
    print("database created successfully!")
    con.commit()
    con.close()


def create_tables():
    con = get_con()
    cursor = con.cursor()
    query_user_details = """CREATE TABLE IF NOT EXISTS user_details (
                                army_no CHAR(8) PRIMARY KEY,
                                full_name VARCHAR(100) NOT NULL,
                                position VARCHAR(100),
                                email VARCHAR(150) UNIQUE NOT NULL,
                                phone VARCHAR(20) UNIQUE,
                                password VARCHAR(255) NOT NULL, 
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                ) """
    query_user_amenities_create = """CREATE TABLE IF NOT EXISTS user_amenities (
                                    id INT PRIMARY KEY AUTO_INCREMENT,
                                    army_no VARCHAR(50) NOT NULL,
                                    item VARCHAR(50) NOT NULL,
                                    quantity INT NOT NULL,
                                    description VARCHAR(1000) DEFAULT "NA",
                                    status ENUM('Pending', 'Accepted', 'Rejected', 'Delayed') DEFAULT 'Pending',
                                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                    FOREIGN KEY (army_no) REFERENCES user_details (army_no)
                                    ) """
    queries = [query_user_details, query_user_amenities_create]
    for num, query in enumerate(queries):
        cursor.execute(query)
        print(f"table {num + 1} created!")
    
    con.commit()
    con.close()


def register_user(army_no, full_name, position, email, phone, password):
    """Register a new user in user_details table"""
    try:
        con = get_con()
        cursor = con.cursor()
        query = """INSERT INTO user_details (army_no, full_name, position, email, phone, password) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (army_no, full_name, position, email, phone, password))
        con.commit()
        con.close()
        return True
    except Exception as e:
        print(f"Error registering user: {e}")
        return False


def user_exists(army_no):
    """Check if user already exists"""
    try:
        con = get_con()
        cursor = con.cursor()
        query = "SELECT * FROM user_details WHERE army_no = %s"
        cursor.execute(query, (army_no,))
        result = cursor.fetchone()
        con.close()
        return result is not None
    except Exception as e:
        print(f"Error checking user: {e}")
        return False


def get_user(army_no):
    """Get user details by army_no"""
    try:
        con = get_con()
        cursor = con.cursor()
        query = "SELECT * FROM user_details WHERE army_no = %s"
        cursor.execute(query, (army_no,))
        result = cursor.fetchone()
        con.close()
        return result
    except Exception as e:
        print(f"Error getting user: {e}")
        return None


def add_demand(army_no, item, quantity, description):
    """Add a demand by user"""
    try:
        con = get_con()
        cursor = con.cursor()
        query = """INSERT INTO user_amenities (army_no, item, quantity, description) 
                   VALUES (%s, %s, %s, %s)"""
        cursor.execute(query, (army_no, item, quantity, description))
        con.commit()
        con.close()
        return True
    except Exception as e:
        print(f"Error adding demand: {e}")
        return False


def get_user_demands(army_no):
    """Get all demands by a user"""
    try:
        con = get_con()
        cursor = con.cursor()
        query = "SELECT * FROM user_amenities WHERE army_no = %s order by created_at desc"
        cursor.execute(query, (army_no,))
        results = cursor.fetchall()
        con.close()
        return results
    except Exception as e:
        print(f"Error getting demands: {e}")
        return []


def get_all_demands():
    """Get all demands (for Store IC)"""
    try:
        con = get_con()
        cursor = con.cursor()
        query = """SELECT ua.id, ua.army_no, ud.full_name, ua.item, ua.quantity, ua.description, ua.status, ua.created_at
                   FROM user_amenities ua
                   JOIN user_details ud ON ua.army_no = ud.army_no
                   ORDER BY ua.created_at DESC"""
        cursor.execute(query)
        results = cursor.fetchall()
        con.close()
        return results
    except Exception as e:
        print(f"Error getting all demands: {e}")
        return []


def update_demand_status(demand_id, status):
    """Update demand status (Pending, Accepted, Rejected, Delayed)"""
    try:
        con = get_con()
        cursor = con.cursor()
        query = "UPDATE user_amenities SET status = %s WHERE id = %s"
        cursor.execute(query, (status, demand_id))
        con.commit()
        con.close()
        return True
    except Exception as e:
        print(f"Error updating demand status: {e}")
        return False

create_tables()