import os

from sqlalchemy import create_engine, text

db_connection_string = os.environ[
    'CONNECTION_STRING']  #enter ur database connection details
engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                           "ssl_ca": "/etc/ssl/cert.pem"
                       }})


def entry(name, email, date, time, people):
  with engine.connect() as conn:
    # SQL query with named placeholders
    sql_query = text(
        "INSERT INTO reservation (name, email, date, time, people) VALUES (:name, :email, :date, :time, :people)"
    )

    # Parameters as a dictionary with named placeholders
    params = {
        'name': name,
        'email': email,
        'date': date,
        'time': time,
        'people': people
    }

    # Execute the SQL query with parameters
    conn.execute(sql_query, params)
