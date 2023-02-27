import requests
import json
import psycopg2
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# Define NASA API endpoint
NASA_API_ENDPOINT = "https://api.nasa.gov/neo/rest/v1/feed"

# Define Airflow DAG
dag = DAG(
    "nasa_asteroids",
    description="Extract information about asteroids from NASA API and load into Redshift data warehouse",
    schedule_interval="0 12 * * *",  # Run the DAG daily at 12:00 UTC
    start_date=datetime(2022, 1, 1),
    catchup=False
)

# Define the function that extracts data from the NASA API
def extract_nasa_asteroids():
    # Define the date range for which to retrieve asteroid data
    start_date = datetime.utcnow().strftime('%Y-%m-%d')
    end_date = (datetime.utcnow() + timedelta(days=7)).strftime('%Y-%m-%d')
    
    # Make request to NASA API
    response = requests.get(f"{NASA_API_ENDPOINT}?start_date={start_date}&end_date={end_date}&api_key=YOUR_API_KEY")
    
    # Convert the JSON response to a Python dictionary
    data = json.loads(response.content)
    
    # Return the asteroid data as a list of dictionaries
    return data['near_earth_objects']

# Define the function that loads the data into Redshift
def load_nasa_asteroids(**kwargs):
    # Connect to the Redshift data warehouse
    conn = psycopg2.connect(
        host='redshift-cluster-1.us-west-2.redshift.amazonaws.com',
        port='5439',
        dbname='mydb',
        user='myuser',
        password='mypassword'
    )
    
    # Open a cursor to execute SQL commands
    cur = conn.cursor()
    
    # Retrieve the asteroid data from the task instance
    asteroids = kwargs['ti'].xcom_pull(task_ids='extract_nasa_asteroids')
    
    # Loop through each asteroid and insert it into the Redshift table
    for asteroid in asteroids:
        cur.execute(f"INSERT INTO nasa_asteroids (name, diameter, velocity, is_hazardous) VALUES ('{asteroid['name']}', {asteroid['estimated_diameter']['meters']['estimated_diameter_max']}, {asteroid['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']}, {asteroid['is_potentially_hazardous_asteroid']})")
    
    # Commit the changes and close the cursor and connection
    conn.commit()
    cur.close()
    conn.close()

# Define the tasks in the DAG
extract_task = PythonOperator(
    task_id='extract_nasa_asteroids',
    python_callable=extract_nasa_asteroids,
    dag=dag
)

load_task = PythonOperator(
    task_id='load_nasa_asteroids',
    python_callable=load_nasa_asteroids,
    provide_context=True,
    dag=dag
)

# Set the task dependencies
extract_task >> load_task
