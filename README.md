# JWT-Authentication Backend with Flask

This is a simple backend project built with `Flask`, implementing an authentication and authorization system with JWT-tokens.

## Features

- **Login (POST /auth/login)**: Authenticate a user and receive access and refresh tokens.
- **Logout (POST /auth/logout)**: Invalidate the access token by adding it to a blacklist.
- **Role-based Access**:
  - `/auth/common`: Content accessible to any authorizated user.
  - `/auth/first-year`: Content accessible only to users with role 1.
  - `/auth/second-year`: Content accessible only to users with role 2.
- JWT-based authentication for secure access.
- Whitelist and blacklist management using Redis.
- In-memory user storage (no database).

## Prerequisites

- Python 3.12
- Redis (can be run locally or via Docker)
- Virtualenv (optional)

## Setup and Installation

### Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kateutkate23/flask-jwt-auth
   cd flask-auth-project
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python3.10 -m venv .venv
   # On Windows: venv\Scripts\activate
   source .venv/bin/activate  
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environmental variables:**

- Create a `.env` file in the project root:
   ```plaintext
   SECRET_KEY=your-secret-key-here
   ```
- Generate a `SECRET_KEY` using Python:
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```
- Copy the generated key into the `.env` file.
5. **Run Redis via Docker:**
  ```bash
  docker run -d -p 6379:6379 redis
  ```
6. **Run the application:**
  ```bash
  python run.py
  ```

The server will run on `http://localhost:5000`.

## Notes
- This project uses in-memory user storage, so user data is hardcoded (username: `testuser`, password: `password`, role: `1`).
- Data in Redis (whitelist and blacklist) will remain until the Redis container is stopped or the token expires.
- See `app/auth/utils.py` for a detailed analysis of potential token leaks and protection measures.

## License
This project is for educational purposes and does not include a specific license.
