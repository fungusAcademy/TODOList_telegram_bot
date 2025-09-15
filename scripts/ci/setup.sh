# scripts/ci/setup.sh
#!/bin/bash
echo "Setting up CI environment..."
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pytest pytest-asyncio pytest-cov