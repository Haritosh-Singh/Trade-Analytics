#!/usr/bin/env python3
"""Test script to verify all imports work correctly"""

try:
    import fastapi
    print("✓ fastapi imported successfully")
except ImportError as e:
    print(f"✗ fastapi import failed: {e}")

try:
    import pandas as pd
    print("✓ pandas imported successfully")
except ImportError as e:
    print(f"✗ pandas import failed: {e}")

try:
    import numpy as np
    print("✓ numpy imported successfully")
except ImportError as e:
    print(f"✗ numpy import failed: {e}")

try:
    import sklearn
    print("✓ sklearn imported successfully")
except ImportError as e:
    print(f"✗ sklearn import failed: {e}")

try:
    import xgboost
    print("✓ xgboost imported successfully")
except ImportError as e:
    print(f"✗ xgboost import failed: {e}")

try:
    import sqlalchemy
    print("✓ sqlalchemy imported successfully")
except ImportError as e:
    print(f"✗ sqlalchemy import failed: {e}")

try:
    import pydantic
    print("✓ pydantic imported successfully")
except ImportError as e:
    print(f"✗ pydantic import failed: {e}")

try:
    import uvicorn
    print("✓ uvicorn imported successfully")
except ImportError as e:
    print(f"✗ uvicorn import failed: {e}")

try:
    import joblib
    print("✓ joblib imported successfully")
except ImportError as e:
    print(f"✗ joblib import failed: {e}")

print("\nAll import tests completed!")
