import urllib.request
import socket

def test_connection():
    try:
        # Test socket connection first
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(('127.0.0.1', 5000))
        sock.close()
        
        if result == 0:
            print("✅ Port 5000 is open and listening")
            
            # Try HTTP request
            try:
                response = urllib.request.urlopen('http://127.0.0.1:5000', timeout=5)
                status_code = response.getcode()
                content = response.read(100)  # Read first 100 bytes
                print(f"✅ HTTP Response: {status_code}")
                print(f"   Content preview: {content[:50]}...")
                return True
            except Exception as e:
                print(f"❌ HTTP Request failed: {e}")
                return False
        else:
            print(f"❌ Port 5000 is not accessible (code: {result})")
            return False
            
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

if __name__ == '__main__':
    print("🧪 Testing Flask application...")
    if test_connection():
        print("\n🎉 Application is responding correctly!")
        print("🌐 Try opening: http://127.0.0.1:5000 in your browser")
    else:
        print("\n❌ Application is not responding")
