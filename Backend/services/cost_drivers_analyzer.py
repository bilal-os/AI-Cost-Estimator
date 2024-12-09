import json
from groq import Groq

class CostDriversAnalyzer:
    def __init__(self, api_key):
        """
        Initialize Groq client for cost drivers analysis
        
        :param api_key: Groq API key
        """
        self.client = Groq(api_key=api_key)
        
        # Detailed descriptions for each cost driver
        self.cost_driver_descriptions = {
            'rely': 'Required Software Reliability: The extent to which the software must be accurate, precise, and meet critical user needs.',
            'data': 'Data Base Size: The size and complexity of the database the software will interact with.',
            'cplx': 'Product Complexity: The intricacy of the software\'s processing, algorithms, and control structures.',
            'time': 'Execution Time Constraint: The percentage of available computer time the software must use for processing.',
            'stor': 'Main Storage Constraint: The amount of main memory required by the software.',
            'pvol': 'Platform Volatility: The stability and expected changes in the software development environment.',
            'acap': 'Analyst Capability: The skill level and experience of the system analysts working on the project.',
            'pcap': 'Programmer Capability: The skill level and experience of the programmers developing the software.',
            'aexp': 'Analyst Experience: The team\'s prior experience with similar types of applications and development environments.',
            'pexp': 'Programmer Experience: The team\'s prior experience with the programming language and development tools.',
            'ltex': 'Language and Tool Experience: The team\'s experience with the specific programming languages and tools being used.',
            'tool': 'Use of Software Tools: The sophistication of the software development tools used in the project.',
            'sced': 'Schedule Constraint: The tightness of the project schedule and potential impact on development effort.'
        }
        
        # Predefined value categories with their COCOMO II numerical multipliers
        self.cost_driver_multipliers = {
            'rely': {
                'VeryLow': 0.82,
                'Low': 0.92,
                'Nominal': 1.00,
                'High': 1.10,
                'VeryHigh': 1.26,
                'ExtraHigh': 1.50
            },
            'data': {
                'VeryLow': 0.90,
                'Low': 0.94,
                'Nominal': 1.00,
                'High': 1.08,
                'VeryHigh': 1.16,
                'ExtraHigh': 1.24
            },
            'cplx': {
                'VeryLow': 0.73,
                'Low': 0.87,
                'Nominal': 1.00,
                'High': 1.17,
                'VeryHigh': 1.34,
                'ExtraHigh': 1.74
            },
            'time': {
                'VeryLow': 1.00,
                'Low': 1.00,
                'Nominal': 1.00,
                'High': 1.11,
                'VeryHigh': 1.30,
                'ExtraHigh': 1.66
            },
            'stor': {
                'VeryLow': 1.00,
                'Low': 1.00,
                'Nominal': 1.00,
                'High': 1.05,
                'VeryHigh': 1.20,
                'ExtraHigh': 1.56
            },
            'pvol': {
                'VeryLow': 1.00,
                'Low': 0.87,
                'Nominal': 1.00,
                'High': 1.15,
                'VeryHigh': 1.30,
                'ExtraHigh': 1.56
            },
            'acap': {
                'VeryLow': 1.42,
                'Low': 1.29,
                'Nominal': 1.00,
                'High': 0.85,
                'VeryHigh': 0.71,
                'ExtraHigh': 0.56
            },
            'pcap': {
                'VeryLow': 1.34,
                'Low': 1.15,
                'Nominal': 1.00,
                'High': 0.88,
                'VeryHigh': 0.76,
                'ExtraHigh': 0.62
            },
            'aexp': {
                'VeryLow': 1.22,
                'Low': 1.10,
                'Nominal': 1.00,
                'High': 0.88,
                'VeryHigh': 0.81,
                'ExtraHigh': 0.67
            },
            'pexp': {
                'VeryLow': 1.19,
                'Low': 1.09,
                'Nominal': 1.00,
                'High': 0.91,
                'VeryHigh': 0.85,
                'ExtraHigh': 0.76
            },
            'ltex': {
                'VeryLow': 1.20,
                'Low': 1.09,
                'Nominal': 1.00,
                'High': 0.91,
                'VeryHigh': 0.84,
                'ExtraHigh': 0.70
            },
            'tool': {
                'VeryLow': 1.17,
                'Low': 1.09,
                'Nominal': 1.00,
                'High': 0.90,
                'VeryHigh': 0.78,
                'ExtraHigh': 0.66
            },
            'sced': {
                'VeryLow': 1.43,
                'Low': 1.14,
                'Nominal': 1.00,
                'High': 1.00,
                'VeryHigh': 1.00,
                'ExtraHigh': 1.00
            }
        }
        
        # Predefined value categories (exact match required)
        self.value_categories = list(self.cost_driver_multipliers['rely'].keys())

    def generate_prompt(self, driver):
        """
        Generate a systematic, comprehensive prompt for inferring cost driver values
        
        :param driver: The cost driver to generate a prompt for
        :return: Detailed, structured prompt for Groq API
        """
        return f"""TASK: Software Project Cost Driver Analysis

OBJECTIVE: 
- Precisely categorize a software development cost driver
- Assign an accurate complexity/impact rating based on detailed criteria

CONTEXT:
Cost drivers are factors that significantly influence the effort and complexity of software development. Your assessment will help estimate project resources and challenges.

SPECIFIC COST DRIVER:
- Driver Name: {driver}
- Description: {self.cost_driver_descriptions.get(driver, 'No description available')}

RATING SCALE (STRICTLY USE THESE VALUES ONLY):
- VeryLow: Minimum impact, lowest complexity, minimal additional effort required
- Low: Slight complexity, minimal additional challenges
- Nominal: Standard, average complexity, typical project considerations
- High: Significant complexity, substantial additional effort needed
- VeryHigh: Extensive complexity, major challenges expected
- ExtraHigh: Extreme complexity, potentially project-critical challenges

CRITICAL INSTRUCTIONS:
1. Analyze the cost driver's characteristics comprehensively
2. Select ONLY ONE rating from the provided scale
3. Your ENTIRE response must be EXACTLY ONE of these values:
   VeryLow, Low, Nominal, High, VeryHigh, or ExtraHigh
4. DO NOT include ANY additional text, explanation, or commentary
5. Base your rating on potential project impact and inherent complexity

RESPONSE FORMAT:
Respond with ONLY the selected rating value. Example: "High"

YOUR RESPONSE: """

    def analyze_null_cost_drivers(self, cost_drivers):
        """
        Analyze cost drivers with null values using Groq API
        
        :param cost_drivers: List of cost drivers with potential null values
        :return: Updated list of cost drivers with inferred values
        """
        # Filter out cost drivers with null values
        null_drivers = [driver for driver in cost_drivers if driver['value'].lower() == 'null']
        
        # Process each null driver
        for driver in null_drivers:
            try:
                # Generate prompt for the specific driver
                prompt = self.generate_prompt(driver['driver'])
                
                # Make API call to Groq
                response = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a precise software project estimation analyst. Provide ONLY the specified value."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    model="llama-3.2-3b-preview",
                    max_tokens=10,
                    temperature=0.7
                )
                
                # Extract and clean the response
                inferred_value = response.choices[0].message.content.strip()
                
                # Validate the response
                if inferred_value in self.value_categories:
                    driver['value'] = inferred_value
                    print(f"Inferred value for {driver['driver']}: {inferred_value}")
                else:
                    # Fallback to Nominal if response is invalid
                    driver['value'] = 'Nominal'
                    print(f"Invalid response for {driver['driver']}, defaulting to Nominal")
            
            except Exception as e:
                print(f"Error processing {driver['driver']}: {str(e)}")
                # Fallback to a default value if inference fails
                driver['value'] = 'Nominal'
        
        return cost_drivers

def process_cost_drivers(cost_drivers, groq_api_key):
    """
    Main function to process cost drivers
    
    :param cost_drivers: List of cost drivers
    :param groq_api_key: Groq API key
    :return: Processed cost drivers with numerical multipliers
    """
    # Initialize the analyzer
    analyzer = CostDriversAnalyzer(groq_api_key)
    
    # Analyze and update null cost drivers
    processed_drivers = analyzer.analyze_null_cost_drivers(cost_drivers)
    
    # Add numerical multipliers to the processed drivers
    for driver in processed_drivers:
        try:
            # Ensure case-insensitive matching
            normalized_value = driver['value'].title()
            
            # Verify the driver and value exist in the multipliers
            if driver['driver'] not in analyzer.cost_driver_multipliers:
                print(f"Warning: Unknown cost driver '{driver['driver']}'")
                driver['numerical_value'] = 1.0  # Default neutral value
                continue
            
            if normalized_value not in analyzer.cost_driver_multipliers[driver['driver']]:
                print(f"Warning: Invalid value '{normalized_value}' for driver '{driver['driver']}'")
                driver['numerical_value'] = 1.0  # Default neutral value
                continue
            
            # Assign the numerical multiplier
            driver['numerical_value'] = analyzer.cost_driver_multipliers[driver['driver']][normalized_value]
        
        except KeyError as e:
            print(f"Error processing driver {driver}: {str(e)}")
            driver['numerical_value'] = 1.0  # Fallback to neutral value
    
    return processed_drivers

# Example usage
if __name__ == "__main__":
    # Sample cost drivers with null values
    sample_cost_drivers = [
        {'driver': 'rely', 'value': 'Null'},
        {'driver': 'data', 'value': 'Null'},
        {'driver': 'cplx', 'value': 'Null'}
    ]
    
    # Replace with your actual Groq API key
    groq_api_key = "your_groq_api_key_here"
    
    # Process the cost drivers
    processed_drivers = process_cost_drivers(sample_cost_drivers, groq_api_key)
    
    # Print the processed drivers with numerical values
    print(json.dumps(processed_drivers, indent=2))