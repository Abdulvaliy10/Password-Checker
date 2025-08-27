#!/usr/bin/env python3
"""
Simple test script to verify the API endpoints.
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_root():
    """Test the root endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Root endpoint: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Root endpoint failed: {e}")
        return False

def test_api_info():
    """Test the API info endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/info")
        print(f"API info: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"API info failed: {e}")
        return False

def test_auth_endpoints():
    """Test authentication endpoints."""
    try:
        # Test username availability
        response = requests.get(f"{BASE_URL}/api/v1/auth/check-username/testuser")
        print(f"Username check: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test email availability
        response = requests.get(f"{BASE_URL}/api/v1/auth/check-email/test@example.com")
        print(f"Email check: {response.status_code}")
        print(f"Response: {response.json()}")
        
        return True
    except Exception as e:
        print(f"Auth endpoints failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing English Learning API...")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health),
        ("Root Endpoint", test_root),
        ("API Info", test_api_info),
        ("Auth Endpoints", test_auth_endpoints),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("Test Results:")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nOverall: {passed}/{total} tests passed")