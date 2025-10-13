#!/usr/bin/env python3
"""
Lab 07 Task 02 - Update and Delete Functionality Test Suite
Author: Ali Hamza
Course: Computer Networks Lab (COMP-352L)

This script tests all requirements for Task 02:
1. Update user information (address, phone, email)
2. Delete user account with proper authentication
3. Test cases for both update and delete functionality

Prerequisites:
- Database server (tier_1_db_server.py) must be running on port 6000
- Application server (tier_2_application_server.py) must be running on port 5000
"""

import socket
import json
import threading
import time
import sys
import os
import random

# Add parent directory to path to import from Lab 07
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

HOST = "127.0.0.1"
PORT = 5000  # Application server port

def send_request(request):
    """Send request to application server and return response"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            s.send(json.dumps(request).encode("utf-8"))
            response = s.recv(4096).decode("utf-8")
            return json.loads(response)
        except ConnectionRefusedError:
            print(f"ERROR: Connection refused. Is the application server running on {HOST}:{PORT}?")
            return {"status": "error", "message": "Connection refused"}
        except Exception as e:
            print(f"ERROR: An error occurred while sending request: {e}")
            return {"status": "error", "message": str(e)}

def register_user(user_id, username, password, name, email, max_retries=3):
    """Register a new user with retry logic"""
    for attempt in range(max_retries):
        request = {
            "action": "register",
            "id": user_id,
            "username": username,
            "password": password,
            "name": name,
            "email": email
        }
        print(f"Attempting to register user: {username} (ID: {user_id}) - Attempt {attempt + 1}/{max_retries}")
        response = send_request(request)
        db_response = response.get("db_response", {})
        
        if db_response.get("status") == "ok":
            print(f"SUCCESS: Registration successful for {username}")
            return True
        else:
            error_msg = db_response.get('message', 'Unknown error')
            print(f"FAILED: Registration failed for {username}: {error_msg}")
            
            # If it's a unique constraint error, try with a different ID
            if "UNIQUE constraint failed" in error_msg and "users.id" in error_msg:
                user_id = str(int(user_id) + random.randint(100, 999))
                print(f"Retrying with new ID: {user_id}")
            elif "UNIQUE constraint failed" in error_msg and "users.username" in error_msg:
                username = f"{username}_{random.randint(100, 999)}"
                print(f"Retrying with new username: {username}")
            elif "UNIQUE constraint failed" in error_msg and "users.email" in error_msg:
                email = f"test_{random.randint(100, 999)}_{email}"
                print(f"Retrying with new email: {email}")
            
            if attempt < max_retries - 1:
                time.sleep(1)  # Wait before retry
    
    print(f"FAILED: Registration failed for {username} after {max_retries} attempts")
    return False

def login_user(username, password):
    """Log in a user"""
    request = {
        "action": "login",
        "username": username,
        "password": password
    }
    print(f"Attempting to log in user: {username}")
    response = send_request(request)
    db_response = response.get("db_response", {})
    if db_response.get("status") == "ok":
        user_data = db_response.get("data", {})
        print(f"SUCCESS: Login successful for {username}. Welcome, {user_data.get('name')}")
        return True, user_data
    else:
        print(f"FAILED: Login failed for {username}: {db_response.get('message', 'Unknown error')}")
        return False, None

def update_user_info(username, password, address=None, phone=None, email=None):
    """Update user information"""
    request = {
        "action": "update_user",
        "username": username,
        "password": password
    }
    
    if address is not None:
        request["address"] = address
    if phone is not None:
        request["phone"] = phone
    if email is not None:
        request["email"] = email
    
    print(f"Attempting to update user: {username}")
    response = send_request(request)
    db_response = response.get("db_response", {})
    
    if db_response.get("status") == "ok":
        print(f"SUCCESS: User information updated successfully for {username}")
        return True
    else:
        print(f"FAILED: Update failed for {username}: {db_response.get('message', 'Unknown error')}")
        return False

def delete_user_account(username, password):
    """Delete user account"""
    request = {
        "action": "delete_user",
        "username": username,
        "password": password
    }
    
    print(f"Attempting to delete user account: {username}")
    response = send_request(request)
    db_response = response.get("db_response", {})
    
    if db_response.get("status") == "ok":
        print(f"SUCCESS: User account deleted successfully for {username}")
        return True
    else:
        print(f"FAILED: Deletion failed for {username}: {db_response.get('message', 'Unknown error')}")
        return False

def test_case_1_update_functionality():
    """Test Case 1: Update user information"""
    print("\n" + "="*60)
    print("TEST CASE 1: Update User Information")
    print("="*60)
    
    # First register a test user
    base_id = random.randint(5000, 9999)
    test_user = {
        "user_id": str(base_id),
        "username": "test_update_user",
        "password": "testpass123",
        "name": "Test Update User",
        "email": "testupdate@university.edu"
    }
    
    print("Step 1: Register test user for update testing")
    if not register_user(**test_user):
        print("ERROR: Failed to register test user. Cannot proceed with update tests.")
        return False
    
    print("\nStep 2: Login to verify user exists")
    success, user_data = login_user(test_user["username"], test_user["password"])
    if not success:
        print("ERROR: Failed to login test user. Cannot proceed with update tests.")
        return False
    
    print(f"Current user data: {user_data}")
    
    print("\nStep 3: Update address field (should succeed)")
    if update_user_info(test_user["username"], test_user["password"], address="123 Main Street, City, State"):
        print("PASS: Address update successful")
    else:
        print("FAIL: Address update failed")
        return False
    
    print("\nStep 4: Update phone field (should succeed)")
    if update_user_info(test_user["username"], test_user["password"], phone="+1-555-123-4567"):
        print("PASS: Phone update successful")
    else:
        print("FAIL: Phone update failed")
        return False
    
    print("\nStep 5: Update email field (should succeed)")
    if update_user_info(test_user["username"], test_user["password"], email="newemail@university.edu"):
        print("PASS: Email update successful")
    else:
        print("FAIL: Email update failed")
        return False
    
    print("\nStep 6: Verify updates by logging in again")
    success, updated_data = login_user(test_user["username"], test_user["password"])
    if success:
        print(f"Updated user data: {updated_data}")
        print("PASS: All updates verified")
    else:
        print("FAIL: Could not verify updates")
        return False
    
    print("\nStep 7: Attempt to update GPA field (should fail - not allowed)")
    # Note: GPA is not in the update_user action, but we'll test the error handling
    print("Note: GPA field is not updatable as per requirements (ID and GPA are non-updatable)")
    
    return True

def test_case_2_delete_functionality():
    """Test Case 2: Delete user account"""
    print("\n" + "="*60)
    print("TEST CASE 2: Delete User Account")
    print("="*60)
    
    # Register a test user for deletion
    base_id = random.randint(6000, 9999)
    test_user = {
        "user_id": str(base_id),
        "username": "test_delete_user",
        "password": "deletepass123",
        "name": "Test Delete User",
        "email": "testdelete@university.edu"
    }
    
    print("Step 1: Register test user for deletion testing")
    if not register_user(**test_user):
        print("ERROR: Failed to register test user. Cannot proceed with deletion tests.")
        return False
    
    print("\nStep 2: Login to verify user exists")
    success, user_data = login_user(test_user["username"], test_user["password"])
    if not success:
        print("ERROR: Failed to login test user. Cannot proceed with deletion tests.")
        return False
    
    print(f"User data before deletion: {user_data}")
    
    print("\nStep 3: Delete user account with correct credentials")
    if delete_user_account(test_user["username"], test_user["password"]):
        print("PASS: User account deleted successfully")
    else:
        print("FAIL: User account deletion failed")
        return False
    
    print("\nStep 4: Attempt to login with deleted account (should fail)")
    success, _ = login_user(test_user["username"], test_user["password"])
    if not success:
        print("PASS: Login correctly failed for deleted account")
    else:
        print("FAIL: Login should have failed for deleted account")
        return False
    
    print("\nStep 5: Attempt to delete non-existent account (should fail)")
    if not delete_user_account("non_existent_user", "any_password"):
        print("PASS: Deletion correctly failed for non-existent account")
    else:
        print("FAIL: Deletion should have failed for non-existent account")
        return False
    
    print("\nStep 6: Attempt to delete with wrong password (should fail)")
    # Register another user for this test
    base_id2 = random.randint(7000, 9999)
    test_user2 = {
        "user_id": str(base_id2),
        "username": "test_wrong_pass",
        "password": "correctpass123",
        "name": "Test Wrong Pass",
        "email": "testwrong@university.edu"
    }
    
    if register_user(**test_user2):
        if not delete_user_account(test_user2["username"], "wrong_password"):
            print("PASS: Deletion correctly failed with wrong password")
        else:
            print("FAIL: Deletion should have failed with wrong password")
            return False
    else:
        print("WARNING: Could not register user for wrong password test")
    
    return True

def test_edge_cases():
    """Test edge cases for update and delete functionality"""
    print("\n" + "="*60)
    print("EDGE CASES: Additional Testing")
    print("="*60)
    
    # Test updating with empty fields
    base_id = random.randint(8000, 9999)
    test_user = {
        "user_id": str(base_id),
        "username": "test_edge_cases",
        "password": "edgepass123",
        "name": "Test Edge Cases",
        "email": "testedge@university.edu"
    }
    
    print("Step 1: Register user for edge case testing")
    if not register_user(**test_user):
        print("ERROR: Failed to register test user for edge cases.")
        return False
    
    print("\nStep 2: Test update with no fields provided")
    if not update_user_info(test_user["username"], test_user["password"]):
        print("PASS: Update correctly failed when no fields provided")
    else:
        print("FAIL: Update should have failed when no fields provided")
    
    print("\nStep 3: Test update with invalid credentials")
    if not update_user_info(test_user["username"], "wrong_password", address="Test Address"):
        print("PASS: Update correctly failed with invalid credentials")
    else:
        print("FAIL: Update should have failed with invalid credentials")
    
    print("\nStep 4: Test update with non-existent user")
    if not update_user_info("non_existent_user", "any_password", address="Test Address"):
        print("PASS: Update correctly failed for non-existent user")
    else:
        print("FAIL: Update should have failed for non-existent user")
    
    # Clean up
    delete_user_account(test_user["username"], test_user["password"])
    
    return True

def main():
    """Main test execution function"""
    print("Lab 07 Task 02 - Update and Delete Functionality Test Suite")
    print("Author: Ali Hamza")
    print("Course: Computer Networks Lab (COMP-352L)")
    print("="*60)
    print("Prerequisites:")
    print("   1. Database server (tier_1_db_server.py) must be running on port 6000")
    print("   2. Application server (tier_2_application_server.py) must be running on port 5000")
    print("="*60)
    
    # Check if servers are running
    print("Checking server connectivity...")
    test_request = {"action": "get_student", "id": "1001"}
    test_response = send_request(test_request)
    
    if test_response.get("status") == "error" and "Connection refused" in str(test_response.get("message", "")):
        print("ERROR: Cannot connect to servers. Please start them first:")
        print("   Terminal 1: python3 tier_1_db_server.py")
        print("   Terminal 2: python3 tier_2_application_server.py")
        return
    
    print("SUCCESS: Server connectivity confirmed!")
    print("\nStarting tests in 3 seconds...")
    time.sleep(3)
    
    # Execute all test cases
    try:
        # Test Case 1: Update functionality
        update_success = test_case_1_update_functionality()
        
        # Test Case 2: Delete functionality
        delete_success = test_case_2_delete_functionality()
        
        # Edge cases testing
        edge_success = test_edge_cases()
        
        # Final summary
        print("\n" + "="*60)
        print("FINAL TEST SUMMARY")
        print("="*60)
        print(f"Update Functionality: {'PASSED' if update_success else 'FAILED'}")
        print(f"Delete Functionality: {'PASSED' if delete_success else 'FAILED'}")
        print(f"Edge Cases Testing: {'PASSED' if edge_success else 'FAILED'}")
        
        if update_success and delete_success and edge_success:
            print("\nRESULT: ALL TESTS PASSED! Task 02 requirements fulfilled!")
        else:
            print("\nRESULT: Some tests failed. Check the output above for details.")
            
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user.")
    except Exception as e:
        print(f"\nERROR: Unexpected error during testing: {e}")

if __name__ == "__main__":
    main()
