# scripts/ci/test.sh
#!/bin/bash
echo "Running tests..."
export DATABASE_DSN="postgresql://test_user:test_password@localhost:5432/test_db"
pytest -v --cov=src --cov-report=xml