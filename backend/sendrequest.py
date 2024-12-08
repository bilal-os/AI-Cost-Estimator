import requests

def send_requirements_file(file_path, url):
    try:
        # Open the file
        with open(file_path, 'rb') as file:
            # Create a dictionary with the file
            files = {'file': file}
            
            # Send POST request to the API
            response = requests.post(url, files=files)
            
            # Check if the request was successful
            if response.status_code == 200:
                print("File sent successfully!")
                print("Response:", response.json())
            else:
                print(f"Error: Received status code {response.status_code}")
                print("Response:", response.text)
    
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except requests.RequestException as e:
        print(f"Error sending request: {e}")

# Usage
file_path = 'req.txt'  # Replace with the actual path to your file
url = 'http://127.0.0.1:5000/parse-requirements'  # Replace if your endpoint is different

send_requirements_file(file_path, url)