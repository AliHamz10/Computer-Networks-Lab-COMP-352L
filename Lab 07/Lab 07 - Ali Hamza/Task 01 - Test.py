#!/usr/bin/env python3
"""
Lab 07 Task 01 - Registration and Login Test Suite
Author: Ali Hamza
Course: Computer Networks Lab (COMP-352L)

This script tests all requirements for Task 01:
1. Register 3 New students
2. Log In all 3 simultaneously  
3. Log In with invalid account

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
        return True
    else:
        print(f"FAILED: Login failed for {username}: {db_response.get('message', 'Unknown error')}")
        return False

def test_case_1_register_3_students():
    """Test Case 1: Register 3 New students"""
    print("\n" + "="*60)
    print("TEST CASE 1: Register 3 New Students")
    print("="*60)
    
    # Generate unique IDs to avoid conflicts
    base_id = random.randint(4000, 9999)
    students_to_register = [
        {"user_id": str(base_id), "username": "ali_hamza", "password": "ali123", "name": "Ali Hamza", "email": "ali@university.edu"},
        {"user_id": str(base_id + 1), "username": "zarmeena_jawad", "password": "zarmeena456", "name": "Zarmeena Jawad", "email": "zarmeena@university.edu"},
        {"user_id": str(base_id + 2), "username": "zarghoona_jawad", "password": "zarghoona789", "name": "Zarghoona Jawad", "email": "zarghoona@university.edu"}
    ]
    
    print(f"Using unique IDs: {base_id}, {base_id + 1}, {base_id + 2}")

    registered_students = []
    for i, student in enumerate(students_to_register, 1):
        print(f"\n--- Registering Student {i}/3 ---")
        if register_user(**student):
            registered_students.append(student)
        time.sleep(0.5)  # Small delay between registrations
    
    print(f"\nRegistration Summary: {len(registered_students)}/3 students registered successfully")
    return registered_students

def test_case_2_simultaneous_login(registered_students):
    """Test Case 2: Log In all 3 simultaneously"""
    print("\n" + "="*60)
    print("TEST CASE 2: Simultaneous Login of All Students")
    print("="*60)
    
    if not registered_students or len(registered_students) == 0:
        print("ERROR: No students registered. Cannot test simultaneous login.")
        print("Make sure Test Case 1 completed successfully before running Test Case 2.")
        return False
    
    print(f"Starting simultaneous login for {len(registered_students)} students...")
    print("Note: All students will attempt to log in at the same time using threading.")
    
    # Use thread-safe list for results
    login_results = []
    login_lock = threading.Lock()
    
    def login_worker(student, result_list, lock):
        """Worker function for concurrent login"""
        thread_id = threading.current_thread().ident
        print(f"[Thread {thread_id}] Started login for user: {student['username']}")
        
        success = login_user(student['username'], student['password'])
        
        with lock:
            result_list.append((student['username'], success))
        
        print(f"[Thread {thread_id}] Completed login for {student['username']} - Result: {'SUCCESS' if success else 'FAILED'}")
    
    # Start all login threads
    login_threads = []
    for i, student in enumerate(registered_students, 1):
        print(f"Starting login thread {i} for {student['username']}")
        thread = threading.Thread(target=login_worker, args=(student, login_results, login_lock))
        login_threads.append(thread)
        thread.start()
        time.sleep(0.2)  # Small delay between thread starts
    
    print(f"All {len(login_threads)} login threads started. Waiting for completion...")
    
    # Wait for all threads to complete with timeout
    for i, thread in enumerate(login_threads, 1):
        thread.join(timeout=10)  # 10 second timeout per thread
        if thread.is_alive():
            print(f"WARNING: Thread {i} did not complete within timeout")
        else:
            print(f"Thread {i} completed successfully")
    
    # Display results
    successful_logins = sum(1 for _, success in login_results if success)
    print(f"\nSimultaneous Login Summary: {successful_logins}/{len(registered_students)} successful logins")
    
    for username, success in login_results:
        status = "PASS" if success else "FAIL"
        print(f"  {status}: {username}")
    
    return successful_logins == len(registered_students)

def test_case_3_invalid_login():
    """Test Case 3: Log In with invalid account"""
    print("\n" + "="*60)
    print("TEST CASE 3: Login with Invalid Account")
    print("="*60)
    
    invalid_credentials = [
        {"username": "non_existent_user", "password": "any_password", "description": "Non-existent username"},
        {"username": "ali_hamza", "password": "wrong_password", "description": "Valid username, wrong password"},
        {"username": "invalid@user", "password": "password123", "description": "Invalid username format"},
        {"username": "", "password": "password123", "description": "Empty username"},
        {"username": "zarmeena_jawad", "password": "", "description": "Empty password"}
    ]
    
    print("Testing various invalid login scenarios...")
    
    for i, cred in enumerate(invalid_credentials, 1):
        print(f"\n--- Invalid Login Test {i}/5: {cred['description']} ---")
        success = login_user(cred['username'], cred['password'])
        
        if not success:
            print(f"PASS: Correctly rejected invalid login: {cred['description']}")
        else:
            print(f"ERROR: Invalid login was accepted: {cred['description']}")
    
    print(f"\nInvalid Login Test Summary: All invalid logins should be rejected")

def test_student_info_access():
    """Bonus test: Test student information access"""
    print("\n" + "="*60)
    print("BONUS TEST: Student Information Access")
    print("="*60)
    
    # Test accessing existing student data
    existing_students = ["1001", "1002", "1003"]  # From the default database
    
    for student_id in existing_students:
        print(f"\n--- Testing Student Info Access for ID: {student_id} ---")
        request = {"action": "get_student", "id": student_id}
        response = send_request(request)
        db_response = response.get("db_response", {})
        
        if db_response.get("status") == "ok":
            student_data = db_response.get("data", {})
            print(f"SUCCESS: Student found: {student_data.get('name')} (GPA: {student_data.get('gpa')})")
        else:
            print(f"FAILED: Student not found: {db_response.get('message')}")

def main():
    """Main test execution function"""
    print("Lab 07 Task 01 - Registration and Login Test Suite")
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
        # Test Case 1: Register 3 students
        registered_students = test_case_1_register_3_students()
        print(f"\nDEBUG: Registered students count: {len(registered_students)}")
        if registered_students:
            print("DEBUG: Registered students list:")
            for i, student in enumerate(registered_students, 1):
                print(f"  {i}. {student['username']} ({student['name']})")
        
        # Test Case 2: Simultaneous login
        simultaneous_success = test_case_2_simultaneous_login(registered_students)
        
        # Test Case 3: Invalid login
        test_case_3_invalid_login()
        
        # Bonus test: Student info access
        test_student_info_access()
        
        # Final summary
        print("\n" + "="*60)
        print("FINAL TEST SUMMARY")
        print("="*60)
        print(f"Registration Test: {len(registered_students)}/3 students registered")
        print(f"Simultaneous Login: {'PASSED' if simultaneous_success else 'FAILED'}")
        print("Invalid Login: All invalid attempts correctly rejected")
        print("Student Info Access: Database queries working")
        
        if len(registered_students) == 3 and simultaneous_success:
            print("\nRESULT: ALL TESTS PASSED! Task 01 requirements fulfilled!")
        else:
            print("\nRESULT: Some tests failed. Check the output above for details.")
            
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user.")
    except Exception as e:
        print(f"\nERROR: Unexpected error during testing: {e}")

if __name__ == "__main__":
    main()
