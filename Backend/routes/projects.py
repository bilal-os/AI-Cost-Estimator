from flask import jsonify
from models.mock_data import MOCK_PROJECTS

def register_projects_routes(app):
    """
    Register routes related to projects
    
    :param app: Flask application instance
    """
    @app.route('/projects', methods=['GET'])
    def get_projects():
        """
        Endpoint to retrieve list of projects
        """
        return jsonify(MOCK_PROJECTS), 200