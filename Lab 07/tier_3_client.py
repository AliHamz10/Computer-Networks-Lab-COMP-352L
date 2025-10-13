import socket
import json

HOST = "127.0.0.1"
PORT = 5000

def send_request(request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(json.dumps(request).encode("utf-8"))
        response = s.recv(4096).decode("utf-8")
        return json.loads(response)

def register_user():
    print("\n=== User Registration ===")
    while True:
        try:
            user_id = input("Enter User ID: ").strip()
            if not user_id:
                print("User ID cannot be empty!")
                continue
                
            username = input("Enter Username: ").strip()
            if not username:
                print("Username cannot be empty!")
                continue
                
            password = input("Enter Password: ").strip()
            if not password:
                print("Password cannot be empty!")
                continue
                
            name = input("Enter Full Name: ").strip()
            if not name:
                print("Name cannot be empty!")
                continue
                
            email = input("Enter Email: ").strip()
            if not email:
                print("Email cannot be empty!")
                continue
            
            request = {
                "action": "register",
                "id": user_id,
                "username": username,
                "password": password,
                "name": name,
                "email": email
            }
            
            response = send_request(request)
            print("\n[Server Response]:")
            print(json.dumps(response, indent=4))
            
            db_response = response.get("db_response", {})
            if db_response.get("status") == "ok":
                print("Registration successful!")
                return True
            else:
                print(f"Registration failed: {db_response.get('message')}")
                retry = input("Try again? (y/n): ").strip().lower()
                if retry != 'y':
                    return False
                    
        except KeyboardInterrupt:
            print("\nRegistration cancelled.")
            return False

def login_user():
    print("\n=== User Login ===")
    while True:
        try:
            username = input("Enter Username: ").strip()
            if not username:
                print("Username cannot be empty!")
                continue
                
            password = input("Enter Password: ").strip()
            if not password:
                print("Password cannot be empty!")
                continue
            
            request = {
                "action": "login",
                "username": username,
                "password": password
            }
            
            response = send_request(request)
            print("\n[Server Response]:")
            print(json.dumps(response, indent=4))
            
            db_response = response.get("db_response", {})
            if db_response.get("status") == "ok":
                user_data = db_response.get("data", {})
                print(f"Login successful! Welcome, {user_data.get('name')}!")
                return True
            else:
                print(f"Login failed: {db_response.get('message')}")
                retry = input("Try again? (y/n): ").strip().lower()
                if retry != 'y':
                    return False
                    
        except KeyboardInterrupt:
            print("\nLogin cancelled.")
            return False

def get_student_info():
    print("\n=== Student Information ===")
    while True:
        try:
            student_id = input("Enter Student ID (or 'back' to return): ").strip()
            if student_id.lower() == "back":
                return
            if not student_id:
                print("Student ID cannot be empty!")
                continue
            
            request = {"action": "get_student", "id": student_id}
            response = send_request(request)
            print("\n[Server Response]:")
            print(json.dumps(response, indent=4))
            
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return

def update_user_info():
    print("\n=== Update User Information ===")
    while True:
        try:
            username = input("Enter Username: ").strip()
            if not username:
                print("Username cannot be empty!")
                continue
                
            password = input("Enter Password: ").strip()
            if not password:
                print("Password cannot be empty!")
                continue
            
            print("\nEnter new information (press Enter to skip):")
            address = input("New Address: ").strip()
            phone = input("New Phone Number: ").strip()
            email = input("New Email: ").strip()
            
            # Only include non-empty fields in the request
            request = {
                "action": "update_user",
                "username": username,
                "password": password
            }
            
            if address:
                request["address"] = address
            if phone:
                request["phone"] = phone
            if email:
                request["email"] = email
            
            response = send_request(request)
            print("\n[Server Response]:")
            print(json.dumps(response, indent=4))
            
            db_response = response.get("db_response", {})
            if db_response.get("status") == "ok":
                print("SUCCESS: User information updated successfully!")
                return True
            else:
                print(f"FAILED: Update failed: {db_response.get('message')}")
                retry = input("Try again? (y/n): ").strip().lower()
                if retry != 'y':
                    return False
                    
        except KeyboardInterrupt:
            print("\nUpdate cancelled.")
            return False

def delete_user_account():
    print("\n=== Delete User Account ===")
    while True:
        try:
            username = input("Enter Username: ").strip()
            if not username:
                print("Username cannot be empty!")
                continue
                
            password = input("Enter Password: ").strip()
            if not password:
                print("Password cannot be empty!")
                continue
            
            # Confirmation prompt
            confirm = input(f"Are you sure you want to delete account '{username}'? This action cannot be undone! (yes/no): ").strip().lower()
            if confirm != 'yes':
                print("Account deletion cancelled.")
                return False
            
            request = {
                "action": "delete_user",
                "username": username,
                "password": password
            }
            
            response = send_request(request)
            print("\n[Server Response]:")
            print(json.dumps(response, indent=4))
            
            db_response = response.get("db_response", {})
            if db_response.get("status") == "ok":
                print("SUCCESS: User account deleted successfully!")
                return True
            else:
                print(f"FAILED: Deletion failed: {db_response.get('message')}")
                retry = input("Try again? (y/n): ").strip().lower()
                if retry != 'y':
                    return False
                    
        except KeyboardInterrupt:
            print("\nDeletion cancelled.")
            return False

def main():
    print("=== Multi-Tier System Client ===")
    print("1. Register New User")
    print("2. Login")
    print("3. Update User Information")
    print("4. Delete User Account")
    print("5. Get Student Info")
    print("6. Exit")
   
    while True:
        try:
            choice = input("\nSelect an option (1-6): ").strip()
            
            if choice == "1":
                register_user()
            elif choice == "2":
                login_user()
            elif choice == "3":
                update_user_info()
            elif choice == "4":
                delete_user_account()
            elif choice == "5":
                get_student_info()
            elif choice == "6":
                request = {"action": "exit"}
                response = send_request(request)
                print("\n[Server Response]:")
                print(json.dumps(response, indent=4))
                print("Goodbye!")
                break
            else:
                print("Invalid choice! Please select 1-6.")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break


if __name__ == "__main__":
    main()
