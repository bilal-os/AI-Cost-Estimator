import json
from datetime import datetime
from flask import jsonify, request
from services.document_extractor import extract_text_from_document
from services.function_point_analysis import FunctionPointAnalyzer
from services.cost_drivers_analyzer import process_cost_drivers
from services.effort_estimation_model import EffortEstimationModel

def register_estimations_routes(app, groq_api_key):
    """
    Register estimation-related routes
    
    :param app: Flask application instance
    :param groq_api_key: API key for Groq
    """
    fpa_analyzer = FunctionPointAnalyzer(groq_api_key)
    effort_model = EffortEstimationModel()  # Initialize the effort estimation model

    @app.route('/estimations', methods=['POST'])
    def generate_estimation():
        """
        Endpoint to handle estimation generation
        Echoes back the received data with a mock estimation result
        """
        try:
            # Log the incoming request data
            print(f"Request Data: {request.form.to_dict()}")
            
            # Extract text from requirements document if provided
            requirements_doc = request.files.get('requirementsDocument')
            extracted_text = ""
            fpa_analysis = {
                "EI": {"count": 0, "examples": []},
                "EO": {"count": 0, "examples": []},
                "EQ": {"count": 0, "examples": []},
                "ILF": {"count": 0, "examples": []},
                "EIF": {"count": 0, "examples": []}
            }
            
            if requirements_doc:
                # Extract text from the document
                extracted_text = extract_text_from_document(requirements_doc)
                print("Extracted Document Text:", extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text)
                
                # Perform Function Point Analysis
                fpa_analysis = fpa_analyzer.analyze_requirements(extracted_text)
                print("Function Point Analysis:", fpa_analysis)

            # Parse and process cost drivers
            cost_drivers = json.loads(request.form.get('costDrivers', '[]'))
            print("Original Cost Drivers:", cost_drivers)

            # Process cost drivers with null values
            processed_cost_drivers = process_cost_drivers(cost_drivers, groq_api_key)
            print("Processed Cost Drivers:", processed_cost_drivers)

            # Calculate effort multiplier as the product of numerical values of processed cost drivers
            effort_multiplier = 1.0
            for driver in processed_cost_drivers:
                effort_multiplier *= driver.get('numerical_value', 1.0)
            print(f"Effort Multiplier: {effort_multiplier}")

            # Calculate project metrics
            estimation_results = fpa_analyzer.calculate_project_metrics(fpa_analysis)
            print("Estimation Results:", estimation_results)
            
            # Update estimation results with the calculated effort multiplier
            estimation_results['effortMultiplier'] = effort_multiplier

            # Get estimated KLOC from project metrics
            estimated_kloc = estimation_results.get('estimatedKLOC', 0)
            print(f"Estimated KLOC: {estimated_kloc}")
            
            # Predict effort using the trained model
            predicted_effort = effort_model.predict_effort(processed_cost_drivers, estimated_kloc)
            print(f"Predicted Effort: {predicted_effort}")
            
            # Calculate development time
            development_time = effort_model.calculate_development_time(predicted_effort, estimated_kloc)
            print(f"Development Time: {development_time}")

            # Update estimation results with predicted effort and time
            estimation_results['developmentEffort'] = predicted_effort
            estimation_results['developmentTime'] = development_time

            # Prepare response 
            response_data = {
                "projectName": "Generated Project",
                "dateCreated": datetime.now().isoformat(),
                "extractedRequirementsText": extracted_text,
                "functionPointAnalysis": {
                    "externalInputs": {
                        "count": fpa_analysis['EI']['count'],
                        "modules": fpa_analysis['EI']['examples']
                    },
                    "externalOutputs": {
                        "count": fpa_analysis['EO']['count'],
                        "modules": fpa_analysis['EO']['examples']
                    },
                    "externalInquiries": {
                        "count": fpa_analysis['EQ']['count'],
                        "modules": fpa_analysis['EQ']['examples']
                    },
                    "internalLogicalFiles": {
                        "count": fpa_analysis['ILF']['count'],
                        "modules": fpa_analysis['ILF']['examples']
                    },
                    "externalInterfaceFiles": {
                        "count": fpa_analysis['EIF']['count'],
                        "modules": fpa_analysis['EIF']['examples']
                    }
                },
                "estimationResults": estimation_results,
                "receivedCostDrivers": cost_drivers,
                "processedCostDrivers": processed_cost_drivers 
            }
            
            return jsonify(response_data), 200
        
        except Exception as e:
            # More detailed error logging
            import traceback
            print("Full Error Traceback:")
            traceback.print_exc()
            return jsonify({
                "error": str(e),
                "traceback": traceback.format_exc()
            }), 400
