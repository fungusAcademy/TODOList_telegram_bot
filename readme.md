# Telegram Task Manager Bot 🤖

Telegram bot for task management built with modern Python architecture patterns. Demonstrates clean code practices, dependency injection, database migrations, and professional CI/CD deployment.

## Technologies & Patterns Used

### Backend Framework
- **Aiogram 3.x** - Modern asynchronous Telegram Bot API framework
- **AsyncPG** - Fast PostgreSQL database driver
- **Dependency Injector** - Dependency injection framework
- **Alembic** - Database migrations tool

### Architecture Patterns
- **MVC (Model-View-Controller)** - Separation of concerns
- **Repository Pattern** - Abstracting data access layer
- **Dependency Injection** - Inversion of control principle
- **Clean Architecture** - Independent of frameworks and UI

### Database & Infrastructure
- **PostgreSQL** - Production-ready relational database
- **Alembic Migrations** - Version-controlled database schema changes
- **Connection Pooling** - Optimized database connections
- **Docker** - Containerization and environment consistency

### Development & Deployment
- **Pytest** - Comprehensive testing suite
- **GitHub Actions** - CI/CD pipeline with multiple workflows
- **CodeQL** - Security analysis and code quality
- **Docker Buildx** - Multi-platform container builds

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 13+
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)

### Installation & Setup

1. **Clone and setup the project**
```bash
git clone https://github.com/fungusAcademy/TODOList_telegram_bot.git
cd TODOList_telegram_bot
```
2. **Install dependencies**
```bash
pip install -r requirements.txt
```
3. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration:
# BOT_TOKEN=your_telegram_bot_token
# DATABASE_DSN=postgresql://user:password@localhost:5432/telegram_bot
```
4. **Initialize the database with Alembic migrations**
```bash
# Run database migrations
alembic upgrade head
# Verify migrations status
alembic current
```
5. **Run the application**
```bash
python main.py
```

## Bot Cammands

 - **/start** - Welcome message and bot introduction

- **/add *task text*** - Add a new task to your list

- **/del *task number*** - Delete task by ID

- **/list** - Show all your tasks

- **/help** - Display help information

## Bot Structure

```
telegram_bot/
├── .github/workflows/          # CI/CD pipelines
│   ├── ci-cd.yml              # Continuous integration
│   ├── codeql.yml             # Security analysis
│   ├── deploy.yml             # Deployment automation
│   └── docker.yml             # Docker build and push
├── database/                   # Database layer
│   ├── pool.py                # Connection pooling management
│   └── __init__.py
├── di/                         # Dependency injection
│   ├── containers.py          # IoC container configuration
│   └── __init__.py
├── handlers/                   # Telegram handlers (Controllers)
│   ├── commands.py            # Bot command handlers
│   └── __init__.py
├── migrations/                 # Database migrations (Alembic)
│   ├── versions/              # Migration versions
│   ├── env.py                 # Migration environment
│   └── script.py.mako         # Migration template
├── models/                     # Data models (Entities)
│   ├── task.py                # Task entity model
│   ├── user.py                # User entity model
│   └── __init__.py
├── repositories/               # Data access layer
│   ├── base.py                # Repository interface
│   ├── task_repository.py     # Task repository interface
│   ├── postgres_task_repository.py  # PostgreSQL implementation
│   └── __init__.py
├── services/                   # Business logic layer
│   ├── task_service.py        # Task management service
│   └── __init__.py
├── tests/                      # Test suite
│   ├── conftest.py            # Test fixtures
│   ├── test_database.py       # Database tests
│   ├── test_handlers.py       # Handler tests
│   └── __init__.py
├── utils/                      # Utility functions
│   ├── backup.py              # Database backup utilities
│   └── retry.py               # Retry decorators
└── scripts/ci/                 # CI scripts
    ├── setup.sh               # CI environment setup
    └── test.sh               # Test execution script
```

## Testing
The project includes a comprehensive test suite
```bash
# Run all tests with coverage reporting
pytest tests/ -v --cov=telegram_bot --cov-report=html

# Run specific test categories
pytest tests/test_database.py -v      # Database layer tests
pytest tests/test_handlers.py -v      # Handler integration tests

# Generate coverage report
open htmlcov/index.html  # View coverage in browser
```

## Database migrations
Using Alembic for schema changes:
```bash
# Create new migration
alembic revision -m "description_of_changes"

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1

# Check current migration state
alembic current
```

**Migration workflow:**
1. Modify models in *models/* directory

2. Generate new migration: ``` alembic revision -m "add_new_field" ```

3. Review and edit generated migration file

4. Apply migration: ``` alembic upgrade head ```

5. Test changes thoroughly

## Deployment Options

**GitHub Actions CI/CD Pipeline**
The project includes multiple workflows:

- CI/CD - Automated testing on push/pull requests

- Docker - Automated container builds and pushes

- CodeQL - Security vulnerability scanning

- Deploy - Production deployment automation

**Environment Variables**

```
env
BOT_TOKEN=your_telegram_bot_token_here
DATABASE_DSN=postgresql://user:password@host:5432/database
```

## Key Features Implemented

- **Database Management** - PostgreSQL with Alembic migrations

- **Connection Pooling** - Optimized database connections

- **Dependency Injection** - Clean, testable architecture

- **Error Handling** - Comprehensive exception management

- **Testing Suite** - Unit tests coverage

- **CI/CD Pipeline** - GitHub Actions automation

- **Containerization** - Docker support

- **Security Scanning** - CodeQL integration

- **Database Backups** - Automated backup utilities

- **Retry Mechanism** - Resilient operation handling

## Professional Skills Demonstrated

This project showcases expertise in:

- **Modern Python Development** - Async/await, type hints, modern patterns

- **Database Management** - PostgreSQL, migrations, connection pooling

- **Testing Strategies** - Unit tests, integration tests, coverage reports

- **CI/CD Pipelines** - GitHub Actions, automated testing and deployment

- **Containerization** - Docker, environment consistency

- **Software Architecture** - Clean architecture, design patterns

- **Production Readiness** - Error handling, logging, monitoring

## Contributing

1. Fork the repository

2. Create a feature branch: `git checkout -b feature/amazing-feature`

3. Commit changes: `git commit -m 'Add amazing feature'`

4. Push to branch: `git push origin feature/amazing-feature`

5. Open a Pull Request

## Licence

This project is open source and available under the [MIT License](licence.md).

## Contact

- [Telegram](https://t.me/fungus_academy)

- [Project Link](https://github.com/fungusAcademy/TODOList_telegram_bot)