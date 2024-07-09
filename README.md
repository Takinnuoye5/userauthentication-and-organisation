# FastAPI Authentication and Organization Management

This is a FastAPI application that provides authentication and organization management functionalities. It includes features such as user registration, user login, and organization creation and management.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [Running Migrations](#running-migrations)
- [Running Tests](#running-tests)
- [API Endpoints](#api-endpoints)
- [License](#license)
- [Contributing](#contributing)

## Features

- User registration with automatic organization creation
- User login with JWT authentication
- Organization management
- Validation error handling with custom error responses

## Requirements

- Python 3.8+
- PostgreSQL
- Heroku CLI (for deployment)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Takinnuoye5/userauthentication-and-organisation.git
cd userauthentication-and-organisation
```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
## Environment Variables
Create a .env file in the root directory of your project and add the following environment variables:
```ini
DATABASE_URL=postgresql://yourusername:yourpassword@localhost/yourdatabase
DATABASE_URL_TEST=postgresql://yourusername:yourpassword@localhost/yourtestdatabase
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=your minutes
```
Note: Do not commit the .env file to version control. It should be added to your .gitignore file.

## Running the Application

1.  Apply database migration
   ```bash
  alembic upgrade head
  ```
2. Run the FastAPI application:
    ```bash
   uvicorn my_authentication_app.main:app --reload
   ```
## Running Migrations
To create new migrations and apply them, use Alembic:

1. Create a new migration:
   ``` bash
   alembic revision --autogenerate -m "Your migration message"

2. Apply migrations:
   ```bash
   alembic upgrade head

## Running Tests

1. To run the tests, use the following command:
   ```bash
    pytest
   ```
2. To run tests with detailed output:
```bash
pytest -v --disable-warnings
```

## API Endpoints

Authentication
Register User: POST /auth/register
Login User: POST /auth/login
Get Current User: GET /auth/users/me

Organizations
Create Organization: POST /api/organisations
Get Organizations: GET /api/organisations
Get Organization by ID: GET /api/organisations/{organisation_id}

## License
This project is licensed under the MIT License.

## Contributing
Fork the repository
Create your feature branch (git checkout -b feature/fooBar)
Commit your changes (git commit -am 'Add some fooBar')
Push to the branch (git push origin feature/fooBar)
Create a new Pull Request
```arduino


This README includes instructions for setting up the project, environment variables, running the application, migrations, tests, and a brief description of the available API endpoints. It also emphasizes that the `.env` file should be created locally and not included in version control.





