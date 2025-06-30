import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Configure host and port from environment variables
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    # Run with debug mode if in development
    app.run(
        host=host,
        port=port,
        debug=os.getenv('FLASK_ENV') == 'development'
    )