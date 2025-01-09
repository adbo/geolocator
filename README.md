# Geolocation Application

A simple API to store and retrieve geolocation data based on an IP address or URL.

## Requirements

* Python 3.11
* Docker and Docker Compose

## Running the Application

1. Clone the repository.
2. Navigate to the project directory.
3. Create `.env` file in the root directory and add your `IPSTACK_API_KEY` or you can define env variable (linux example: `export IPSTACK_API_KEY=12345`)
4. Run the application using Docker Compose:

```bash
docker-compose up --build
```

The application will be accessible at `http://localhost:8000`.

## API Endpoints

* **GET /api/v1/geolocations/{ip_or_url}**: Retrieve geolocation data for a given IP or URL from the database.
  ```
  GET http://localhost:8000/api/v1/geolocations/8.8.8.8
  GET http://localhost:8000/api/v1/geolocations/example.com
  ```
* **POST /api/v1/geolocations**:  Create geolocation data in the database with data from ipstack, retrive data from db if already exists (requires `{"ip_or_url": "ip_address_or_url"}` in the request body).
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"ip_or_url": "8.8.8.8"}' http://localhost:8000/api/v1/geolocations
  curl -X POST -H "Content-Type: application/json" -d '{"ip_or_url": "example.com"}' http://localhost:8000/api/v1/geolocations
  ```
* **DELETE /api/v1/geolocations/{ip_or_url}**: Delete geolocation data from the database.
  ```bash
  curl -X DELETE http://localhost:8000/api/v1/geolocations/8.8.8.8
  curl -X DELETE http://localhost:8000/api/v1/geolocations/example.com
  ```

## Running Tests

You can run tests with command:

```bash
docker-compose run test
```

Tests are automaticaly executed when you start docker-compose up, you should see somewhere in the console
```
test_1  | tests/test_endpoints.py ........                                         [100%]
```
