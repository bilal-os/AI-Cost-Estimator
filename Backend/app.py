import os
from flask import Flask
from flask_cors import CORS
from routes.projects import register_projects_routes
from routes.estimations import register_estimations_routes

# Load Groq API key from environment variable
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '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')

# Create Flask application
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Register routes
register_projects_routes(app)
register_estimations_routes(app, GROQ_API_KEY)

if __name__ == '__main__':
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)