from app_production import app
import os

# Set production environment
os.environ.setdefault('FLASK_ENV', 'production')

# Vercel handler
def handler(request):
    environ = request.environ
    start_response = request.start_response
    return app(environ, start_response)

# For local testing
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
