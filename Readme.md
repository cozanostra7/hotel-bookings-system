# Hotel Booking System

A comprehensive hotel booking system built with FastAPI, PostgreSQL, Redis, and Celery.

## Features

- 🏨 Hotel and Room Management
- 📅 Booking System
- 🔐 User Authentication & Authorization (JWT)
- 🎯 Facilities Management
- ⚡ Redis Caching for improved performance
- 📊 Database Migrations with Alembic
- 🔄 Background Tasks with Celery
- 📝 API Documentation with Swagger UI

## Tech Stack

- **Backend Framework:** FastAPI
- **Database:** PostgreSQL
- **Cache & Message Broker:** Redis
- **Task Queue:** Celery
- **ORM:** SQLAlchemy (async)
- **Migration Tool:** Alembic
- **Authentication:** JWT (JSON Web Tokens)
- **Password Hashing:** Bcrypt



## Prerequisites

- Python 3.11+
- PostgreSQL 12+
- Docker (for Redis)
- Git

## Installation

### 1. Clone the Repository

```bash
git clone <https://github.com/cozanostra7/hotel-bookings-system>
cd hotel booking system
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DB_NAME=hotel_booking
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=your_password

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Start Redis with Docker

```bash
docker run -d -p 6379:6379 --name redis redis:alpine
```

Verify Redis is running:
```bash
docker ps
docker exec -it redis redis-cli ping
# Should return: PONG
```

### 6. Set Up PostgreSQL Database

Create a new database:
```sql
CREATE DATABASE hotel_booking;
```

### 7. Run Database Migrations

```bash
# Create initial migration
alembic revision --autogenerate -m "initial migration"

# Apply migrations
alembic upgrade head
```

## Running the Application

### 1. Start FastAPI Server

```bash
python src/main.py
```

The API will be available at: `http://localhost:8003`

### 2. Start Celery Worker (Optional, for background tasks)

In a separate terminal:

```bash
# Activate virtual environment first
venv\Scripts\activate

# Start Celery worker (Windows)
celery -A src.tasks.celery_app:celery_instance worker --loglevel=info --pool=solo

# On macOS/Linux
celery -A src.tasks.celery_app:celery_instance worker --loglevel=info
```

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI:** http://localhost:8003/docs

## Database Migrations

### Create a New Migration

```bash
alembic revision --autogenerate -m "description of changes"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Migration

```bash
# Rollback one step
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>
```

### View Migration History

```bash
alembic history
```

### Check Current Version

```bash
alembic current
```

## Development

### Code Structure

- **Models:** SQLAlchemy ORM models in `src/models/`
- **Schemas:** Pydantic models for request/response validation in `src/schemas/`
- **Repositories:** Database access layer in `src/repositories/`
- **Services:** Business logic in `src/services/`
- **API Routes:** FastAPI endpoints in `src/api/`

### Adding a New Feature

1. Create the database model in `src/models/`
2. Create Pydantic schemas in `src/schemas/`
3. Create repository in `src/repositories/`
4. Create API routes in `src/api/`
5. Generate and apply migration:
   ```bash
   alembic revision --autogenerate -m "add new feature"
   alembic upgrade head
   ```

