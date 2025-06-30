from app import create_app

app = create_app()

if __name__ == '__main__':
    # Only use debug mode locally
    app.run(debug=os.getenv('FLASK_ENV') == 'development')