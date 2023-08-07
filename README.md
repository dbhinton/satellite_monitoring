# Satellite Monitoring

This is a Django application that allows users to register, login, and download and/or delete their data.

## Getting Started

1. Clone the repository to your local machine.
2. Create a virtual environment and activate it.
3. Install the dependencies by running the following command:

pip install -r requirements.txt


4. Migrate the database by running the following command:

python manage.py migrate


5. Run the development server by running the following command:

python manage.py runserver

The development server will be running on port 8000. You can access the application at 

http://127.0.0.1:8000/api/stats/

and

http://127.0.0.1:8000/api/health

1. At /stats you can view the min, max and avg altitude for data fetched from Carsfast satellite endpoint

2. At /health you can view the health of the satellite

