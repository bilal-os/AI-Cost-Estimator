from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import json
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Mock Projects Data
MOCK_PROJECTS = [
    {
        "projectName": "Inventory Manager",
        "dateCreated": (datetime.now() - timedelta(days=30)).isoformat(),
        "functionPointAnalysis": {
            "externalInputs": {
                "count": 3,
                "modules": ["Login form", "Customer entry", "File upload"]
            },
            "externalOutputs": {
                "count": 2,
                "modules": ["Order confirmation", "Sales report"]
            },
            "externalInquiries": {
                "count": 1,
                "modules": ["Product search"]
            },
            "internalLogicalFiles": {
                "count": 2,
                "modules": ["Employee records", "Product catalog"]
            },
            "externalInterfaceFiles": {
                "count": 1,
                "modules": ["Currency exchange API"]
            }
        },
        "estimationResults": {
            "projectSize": 120,
            "developmentEffort": 150,
            "effortMultiplier": 1.2,
            "developmentTime": 18
        }
    },
    {
        "projectName": "E-commerce Platform",
        "dateCreated": (datetime.now() - timedelta(days=45)).isoformat(),
        "functionPointAnalysis": {
            "externalInputs": {
                "count": 4,
                "modules": ["User registration", "Product listing", "Cart management", "Checkout"]
            },
            "externalOutputs": {
                "count": 3,
                "modules": ["Order confirmation", "Shipping update", "Invoice generation"]
            },
            "externalInquiries": {
                "count": 2,
                "modules": ["Product search", "Order tracking"]
            },
            "internalLogicalFiles": {
                "count": 3,
                "modules": ["User profiles", "Product catalog", "Order history"]
            },
            "externalInterfaceFiles": {
                "count": 2,
                "modules": ["Payment gateway", "Shipping API"]
            }
        },
        "estimationResults": {
            "projectSize": 200,
            "developmentEffort": 250,
            "effortMultiplier": 1.5,
            "developmentTime": 24
        }
    }
]

@app.route('/projects', methods=['GET'])
def get_projects():
    """
    Endpoint to retrieve list of projects
    """
    return jsonify(MOCK_PROJECTS), 200

@app.route('/estimations', methods=['POST'])
def generate_estimation():
    """
    Endpoint to handle estimation generation
    Echoes back the received data with a mock estimation result
    """
    try:
        # Handle file upload
        requirements_doc = request.files.get('requirementsDocument')
        
        # Parse cost drivers
        cost_drivers = json.loads(request.form.get('costDrivers', '[]'))

        # Log received files and form data
        print("Received Request Data:")
        print("Files:", request.files)
        print("Form Data:", request.form)

        # Handle file upload
        requirements_doc = request.files.get('requirementsDocument')
        if requirements_doc:
            print(f"Received file: {requirements_doc.filename}")

        # Parse cost drivers
        cost_drivers = json.loads(request.form.get('costDrivers', '[]'))
        print("Parsed Cost Drivers:", cost_drivers)
        
        # Prepare response (mimic an estimation result)
        response_data = {
            "projectName": "Generated Project",
            "dateCreated": datetime.now().isoformat(),
            "functionPointAnalysis": {
                "externalInputs": {
                    "count": len([d for d in cost_drivers if 'input' in d['driver'].lower()]),
                    "modules": ["Dynamically Generated Module"]
                },
                "externalOutputs": {
                    "count": len([d for d in cost_drivers if 'output' in d['driver'].lower()]),
                    "modules": ["Output Module"]
                },
                "externalInquiries": {
                    "count": 1,
                    "modules": ["Query Module"]
                },
                "internalLogicalFiles": {
                    "count": 2,
                    "modules": ["Internal Records"]
                },
                "externalInterfaceFiles": {
                    "count": 1,
                    "modules": ["External Integration"]
                }
            },
            "estimationResults": {
                "projectSize": len(cost_drivers) * 10,
                "developmentEffort": len(cost_drivers) * 15,
                "effortMultiplier": 1.3,
                "developmentTime": len(cost_drivers) * 2
            },
            "receivedCostDrivers": cost_drivers
        }
        
        return jsonify(response_data), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)