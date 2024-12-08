from flask import Flask, request, jsonify
import json
from llamaapi import LlamaAPI

app = Flask(__name__)

# Initialize the SDK
llama = LlamaAPI("")

@app.route('/parse-requirements', methods=['POST'])
def parse_requirements():
    try:
        print("Request Headers:", request.headers)
        print("Request Form:", request.form)
        print("Request Files:", request.files)
        # Get the uploaded file from the request
        file = request.files.get('file')
        if not file:
            return jsonify({"error": "No file provided"})
        
    
        file_content = file.read().decode('utf-8')

        # Build the API request
        api_request_json = {
            "model": "llama3.1-70b",
            "messages": [
                {
                    "role": "user",
                    "content": f"Parse the following requirements document to extract COCOMO cost driver values:\n{file_content}",
                },
            ],
            "functions": [
                {
                    "name": "extract_cocomo_cost_driver",
                    "description": "Extract the numerical value of the COCOMO cost driver from a requirements document.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "cost_driver": {
                                "type": "string",
                                "description": "The name of the COCOMO cost driver extracted.",
                            },
                            "value": {
                                "type": "number",
                                "description": "The numerical value of the cost driver.",
                            },
                        },
                    },
                    "required": ["cost_driver", "value"],
                },
            ],
            "stream": False,
            "function_call": "extract_cocomo_cost_driver",
        }

        # Execute the request
        response = llama.run(api_request_json)
        return jsonify(response.json()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
