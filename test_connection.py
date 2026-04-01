import requests
import time

def test_app():
    """Test if the Flask app is responding"""
    urls = [
        'http://127.0.0.1:5000',
        'http://localhost:5000',
        'http://127.0.0.1:5000/'
    ]
    
    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            print(f"✅ {url} - Status: {response.status_code}")
            if response.status_code == 200:
                print(f"   Content length: {len(response.text)} characters")
                return True
        except requests.exceptions.ConnectionError as e:
            print(f"❌ {url} - Connection Error: {e}")
        except requests.exceptions.Timeout as e:
            print(f"❌ {url} - Timeout: {e}")
        except Exception as e:
            print(f"❌ {url} - Error: {e}")
    
    return False

if __name__ == '__main__':
    print("🧪 Testing Flask application connectivity...")
    print("Waiting 2 seconds for app to start...")
    time.sleep(2)
    
    if test_app():
        print("\n✅ Application is accessible!")
    else:
        print("\n❌ Application is not accessible. Check if app is running.")
