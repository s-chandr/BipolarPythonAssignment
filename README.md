# BiPolar Project API Documentation

This document provides an overview of the API endpoints and their functionalities in the BiPolar project.

## Requirements

To run the project, you need the following:

- Python
- Flask
- Flask-RESTful
- pymongo
- flask_jwt_extended
- bcrypt

Make sure you have these dependencies installed in your Python environment.

## STEPS TO RUN THE PROJECT 
clone the repo 
`pip install -r requirements.txt`
`python wsgi.py`

## Note : 
In order to serve the front-end go to templates folder it in a seperate terminal :
'python -m http.server 8000'


## API Endpoints

### Flights

#### GET /flight

- Description: Retrieve flight information based on the provided query parameter `flight_number`. If no `flight_number` is provided, it returns a list of all flights.
- Query Parameters:
  - `flight_number` (optional): The flight number to retrieve details for.
- Response:
  - If `flight_number` is provided and a flight with that number exists, it returns flight details as a JSON response with status code 200.
  - If `flight_number` is not provided, it returns a list of all flights as a JSON response with status code 200.
  - If the flight with the given `flight_number` is not found, it returns a JSON response with a message "Flight not found" and status code 404.

#### POST /flight

- Description: Allows admins to register new flights.
- Request Body: The request body should be a JSON object with the following fields:
  - `admin_email`: The email address of the admin registering the flight.
  - `departure_time`: The departure time of the flight in the format "YYYY-MM-DDTHH:MM:SS".
- Authorization: This endpoint requires a valid JWT token with admin privileges. The token should be included in the request headers.
- Response:
  - If the admin email is valid and the departure time is provided, it registers a new flight and returns flight details as a JSON response with status code 200.
  - If the admin email is not valid or missing, it returns a JSON response with a message "Unauthorized access" and status code 400.
  - If there is any other error during flight registration, it returns a JSON response with a message "Something went wrong" and status code 500.

#### DELETE /flight

- Description: Allows admins to delete flights based on the provided query parameter `flight_number`.
- Query Parameters:
  - `flight_number` (required): The flight number of the flight to be deleted.
- Authorization: This endpoint requires a valid JWT token with admin privileges. The token should be included in the request headers.
- Response:
  - If `flight_number` is provided and the flight exists, it deletes the flight and returns a JSON response with a message "Flight with flight_number '{flight_number}' has been deleted" and status code 200.
  - If `flight_number` is missing or not found, it returns a JSON response with a message "Flight not found" and status code 404.
  - If there is any other error during flight deletion, it returns a JSON response with a message "Something went wrong" and status code 500.

### Bookings

#### GET /booking

- Description: Retrieve booking information based on the provided query parameter `email`. It returns a list of bookings associated with the specified `email`.
- Query Parameters:
  - `email` (required): The email address of the user to retrieve bookings for.
- Response:
  - If `email` is provided, it returns a list of bookings as a JSON response with status code 200.
  - If `email` is missing or not found, it returns a JSON response with a message "Email not found" and status code 404.
  - If there is any error during retrieval, it returns a JSON response with a message "Something went wrong" and status code 500.

#### POST /booking

- Description: Allows users to make flight bookings.
- Query Parameters:
  - `flight_number` (required): The flight number of the flight to be booked.
  - `seats` (optional, default: 1): The number of seats to book. Defaults to 1 if not provided.
- Authorization: This endpoint requires a valid JWT token. The token should be included in the request headers.
- Response:
  - If the flight number is valid, seats are available, and the booking is successful, it returns booking details as a JSON response with status code 200.
  - If the flight number is missing or not found, it returns a JSON response with a message "Flight not found" and status code 404.
  - If there are not enough seats available, it returns a JSON response with a message "Flight has {seats} seats vacant. Cannot make a booking." and status code 409.
  - If there is any other error during booking, it returns a JSON response with a message "Something went wrong" and status code 500.

### Users

#### GET /users

- Description: Retrieve information about all registered users.
- Response:
  - If there are registered users, it returns a list of user data as a JSON response with status code 200.
  - If there are no registered users, it returns an empty list as a JSON response with status code 200.
  - If there is any error during retrieval, it returns a JSON response with a message "Something went wrong" and status code 500.

#### POST /users

- Description: Allows users to register with the system.
- Request Body: The request body should be a JSON object with the following fields:
  - `email` (required): The email address of the user.
  - `password` (required): The user's password.
- Response:
  - If the registration is successful, it returns a JSON response with a message "User created" and status code 200. The response also includes an access token and a refresh token that can be used for authentication in subsequent requests.
  - If there is any error during registration, it returns a JSON response with a message "Something went wrong" and status code 500.

#### GET /users/<email>

- Description: Retrieve information about a specific user based on the provided email.
- Path Parameters:
  - `email` (required): The email address of the user to retrieve information for.
- Response:
  - If the user with the provided email exists, it returns user data as a JSON response with status code 200.
  - If the user with the provided email is not found, it returns a JSON response with a message "User not found" and status code 404.
  - If there is any error during retrieval, it returns a JSON response with a message "Something went wrong" and status code 500.

#### PUT /users/<email>

- Description: Allows users to update their profile.
- Path Parameters:
  - `email` (required): The email address of the user to update.
- Request Body: The request body should be a JSON object with the fields that need to be updated.
- Response:
  - If the user is found and the profile is updated successfully, it returns a JSON response with a message "User updated" and status code 200.
  - If the user with the provided email is not found, it returns a JSON response with a message "User not found" and status code 404.
  - If there is any error during the update, it returns a JSON response with a message "Something went wrong" and status code 500.

#### DELETE /users/<email>

- Description: Allows users to delete their account.
- Path Parameters:
  - `email` (required): The email address of the user to delete.
- Response:
  - If the user is found and the account is deleted successfully, it returns a JSON response with a message "User deleted" and status code 200.
  - If the user with the provided email is not found, it returns a JSON response with a message "User not found" and status code 404.
  - If there is any error during deletion, it returns a JSON response with a message "Something went wrong" and status code 500.

#### POST /login

- Description: Allows users to log in with their credentials.
- Request Body: The request body should be a JSON object with the following fields:
  - `email` (required): The email address of the user.
  - `password` (required): The user's password.
- Response:
  - If the login is successful, it returns a JSON response with a message "User Login" and status code 200. The response also includes an access token and a refresh token that can be used for authentication in subsequent requests.
  - If the login credentials are invalid, it returns a JSON response with a message "Invalid credentials" and status code 401.
  - If there is any error during login, it returns a JSON response with a message "Something went wrong" and status code 500.

#### POST /logout

- Description: Allows users to log out and revoke their access token.
- Authorization: This endpoint requires a valid JWT token. The token should be included in the request headers.
- Response:
  - If the logout is successful, it returns a JSON response with a message "Logout Success" and status code 200.
  - If the access token is invalid or the user is not authorized, it returns a JSON response with a message "Invalid Token" and status code 403.
  - If there is any error during logout, it returns a JSON response with a message "Something went wrong" and status code 500.

## License

This code is licensed under the MIT License. Feel free to use and modify it according to your needs.
