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

def main():
    print("=== Student Info Client ===")
   
    while True:
        
        student_id = input("Enter Student ID: ").strip()
        if student_id.lower() == "exit":
            request = {"action": "exit"}
            response = send_request(request)
            print("\n[Server Response]:")
            print(json.dumps(response, indent=4))
            break
        
        request = {"action": "get_student", "id": student_id}
        
        response = send_request(request)
        print("\n[Server Response]:")
        print(json.dumps(response, indent=4))


if __name__ == "__main__":
    main()
