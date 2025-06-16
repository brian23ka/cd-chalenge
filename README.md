# Superheroes API


Welcome to the Superheroes API! This project is a simple Flask-based REST API for tracking comic book heroes and their amazing superpowers. It was built as part of a code challenge to practice building relationships, validations, and RESTful endpoints in Flask.

---

## Owner

**Brian kaloki**

---

## Project Overview

This API lets you:

- List all heroes and their super names
- View detailed info about a hero, including their powers and strengths
- List all available powers
- View and update a specific power’s description
- Assign powers to heroes with a strength rating
- Get clear error messages for invalid requests

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Setup Instructions

1. **Clone this repository**
    ```sh
    git clone [ssh-key]
    cd [repo name]
    ```

2. **Create and activate a virtual environment**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**
    ```sh
    pipenv  install -r requirements.txt
    pipenv shell to activate also the environment  
    ```

4. **Set up the database**
    ```sh
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

5. **Seed the database**
    - If you have a seed file, run PYTHONPATH=. python app/seed.py.
    - Or, add your own heroes and powers using the API!

6. **Start the server**
    ```sh
    python run.py
    ```

7. **Test the API**
    - Import the provided Postman collection (`challenge-2-superheroes.postman_collection.json`) into Postman or the Postman VS Code extension.
    - Try out the endpoints and see the responses.

---

## Example Endpoints

- `GET /heroes` — List all heroes
- `GET /heroes/<id>` — Get a hero and their powers
- `GET /powers` — List all powers
- `GET /powers/<id>` — Get a specific power
- `PATCH /powers/<id>` — Update a power’s description
- `POST /hero_powers` — Assign a power to a hero

---

## Contact

If you have any questions or run into issues, feel free to reach out:  
**Email:** brian.kaloki@gmail.com

---

## License

MIT License. See the [LICENSE](LICENSE) file for details.

---

Thanks for checking out my project!