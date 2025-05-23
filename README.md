# Project Template API

This is a FastAPI project template designed to be the foundational base for all future projects. Built following industry best practices for building scalable, modular, and production-ready applications, this template includes ready-to-use components for API routing, authentication (using JWT), logging, background task processing using Celery, and MongoDB integration. It is ideally suited for developing microservices or full-stack systems that require a robust and maintainable API structure.

## Features

- **FastAPI Framework:** A modern, high-performance web framework for building APIs with Python.
- **JWT Authentication:** Secure route protection using OAuth2 and JWT with password hashing.
- **Celery Integration:** Built-in support for asynchronous background task processing using Celery.
- **MongoDB Connectivity:** Utilities for establishing and managing a MongoDB connection.
- **Logging:** Centralized, customizable logging configuration to ensure effective monitoring.
- **Docker & Docker Compose:** Containerized setup for seamless deployment and scalability.
- **Modular Project Structure:** A clean, reproducible folder layout that serves as a base template for future projects.
- **Environment Configuration:** Managed via dotenv to securely handle sensitive credentials.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Docker and Docker Compose (for containerized deployment)

### Installation

1. **Clone the Repository:**

```bash
git clone https://github.com/Y4rd13/fastapi-project-template.git
```

2. **Install Dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run the Application Locally:**

To run the FastAPI application using Uvicorn:

```bash
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```

Or, to run the application inside Docker using Docker Compose:

```bash
docker-compose up --build
```

### Project Structure

```bash
.
├── .env
├── .gitignore
├── .dockerignore
├── docker-compose.yaml
├── Dockerfile
├── README.md
├── requirements.txt
├── pytest
│   └── test_api.py
├── scripts
│   ├── generate_secret.py
│   └── test_cuda.py
└── src
    ├── app.py
    ├── core
    │   ├── config.py
    │   ├── __init__.py
    │   ├── log_config.py
    │   └── logger_func.py
    ├── __init__.py
    ├── models
    │   ├── auth.py
    │   ├── __init__.py
    │   └── requests.py
    ├── routers
    │   ├── auth.py
    │   ├── health.py
    │   ├── __init__.py
    │   ├── task_status.py
    │   └── your_service_route.py
    ├── services
    │   ├── celery.py
    │   ├── __init__.py
    │   ├── tasks.py
    │   └── your_service.py
    └── utils
        ├── auth_utils.py
        ├── __init__.py
        └── mongo_utils.py
```

### Configuration

Sensitive configurations are managed via environment variables. Create a `.env` file at the root of the project (or use a secrets manager in production) with content similar to:

```bash
SECRET_KEY="your_secret_key_here"
MONGO_URI="mongodb://localhost:27017/your_db_name"
```

Both the secret key and the hashed password can be generated using the script in `scripts/generate_secret.py`.

### Creating a Superuser in MongoDB

To initialize your user database, you should create a superuser with the following schema:

```python
from pydantic import BaseModel
from typing import Union

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class User(BaseModel):
    username: str
    email: Union[str, None] = None
    disabled: Union[bool, None] = None

class UserInDB(User):
    hashed_password: str
    is_active: bool
    is_staff: bool
    is_superuser: bool
```

The first superuser should have:

* username: a unique identifier
* email: contact email address
* hashed_password: generated via scripts/generate_secret.py
* is_active: True
* is_staff: True
* is_superuser: True

Superuser (using the UserInDB schema):
```json
{
  "username": "admin",
  "email": "admin@example.com",
  "disabled": false,
  "hashed_password": "hashed_password_value_here",
  "is_active": true,
  "is_staff": true,
  "is_superuser": true
}
```

Regular User (using the User schema):
```json
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "disabled": false
}
```

### CI/CD Deployment

A GitHub Actions workflow template is provided in `.github/workflows/sv_deploy.yaml` to facilitate automated deployment. The workflow performs the following steps:
- Checks out the code.
- Creates a release tag.
- Sets up SSH access to your production server.
- Synchronizes the repository on the server.
- Restarts the Docker containers using `docker-compose`.

### Running Tests

Unit and integration tests are located in the `tests/` directory. You can run tests with:

```bash
pytest
```

## Contributing

Contributions are welcome! Please follow these best practices:
- Use clear, descriptive commit messages.
- Write unit tests for any new features.
- Ensure your code adheres to PEP8 guidelines and the project’s coding standards.

## License

This project template is open source and available under the [MIT License](LICENSE).

---

For additional details, refer to the inline documentation within each module. This template is designed to accelerate your project development by providing a consistent base structure that includes best practices for JWT-based authentication and Celery integration for asynchronous background tasks. Happy coding!
