import pandas as pd
import numpy as np
import tensorflow as tf
import pickle
from sklearn.preprocessing import MinMaxScaler

class EffortEstimationModel:
    def __init__(self, model_path='cocomo_effort_model.keras', scaler_X_path='scaler_X.pkl', scaler_y_path='scaler_y.pkl'):
        """
        Initialize the Effort Estimation Model
        
        :param model_path: Path to the saved TensorFlow model
        :param scaler_X_path: Path to the saved MinMaxScaler for input features
        :param scaler_y_path: Path to the saved MinMaxScaler for output labels
        """
        # Load the pre-trained model
        self.model = tf.keras.models.load_model(model_path)
        
        # Load scalers
        self.scaler_X = self._load_scaler(scaler_X_path)
        self.scaler_y = self._load_scaler(scaler_y_path)
        
        # Predefined order of cost drivers for consistent input
        self.cost_driver_order = [
            'rely', 'data', 'cplx', 'time', 'stor', 'pvol', 
            'acap', 'pcap', 'aexp', 'pexp', 'ltex', 'tool', 
            'sced', 'virt', 'turn'
        ]

    def _load_scaler(self, scaler_path):
        """
        Load a MinMaxScaler from a file or return a default instance if no path is provided.
        
        :param scaler_path: Path to the saved scaler file
        :return: Loaded MinMaxScaler or a default MinMaxScaler
        """
        try:
            with open(scaler_path, 'rb') as f:
                return pickle.load(f)
        except (FileNotFoundError, IOError):
            print(f"Warning: Could not load scaler from {scaler_path}. Using default MinMaxScaler.")
            return MinMaxScaler()

    def prepare_input(self, processed_cost_drivers, estimated_kloc):
        """
        Prepare input for the model with proper feature names
        
        :param processed_cost_drivers: List of cost drivers
        :param estimated_kloc: Estimated thousands of lines of code
        :return: Scaled input features
        """
        # Create a dictionary of cost drivers for easy lookup
        cost_driver_dict = {driver['driver']: driver['numerical_value'] for driver in processed_cost_drivers}
        
        # Prepare input features in the predefined order
        input_features = [
            cost_driver_dict.get(driver, 1.0)  # Default to 1.0 if driver not present
            for driver in self.cost_driver_order
        ]
        
        # Add estimated KLOC as the last feature
        input_features.append(estimated_kloc)
        
        # Convert to NumPy array
        X = np.array(input_features).reshape(1, -1)
        
        # Scale the input features
        X_scaled = self.scaler_X.transform(X)
        
        return X_scaled

    def predict_effort(self, processed_cost_drivers, estimated_kloc):
        """
        Predict effort using the trained model
        
        :param processed_cost_drivers: List of processed cost drivers
        :param estimated_kloc: Estimated thousands of lines of code
        :return: Predicted effort as a standard Python float
        """
        # Prepare scaled input
        X_scaled = self.prepare_input(processed_cost_drivers, estimated_kloc)
        
        # Make prediction
        effort_scaled = self.model.predict(X_scaled)
        
        # Inverse transform to get actual effort and convert to standard Python float
        effort = float(self.scaler_y.inverse_transform(effort_scaled)[0][0])
        
        return effort

    def calculate_development_time(self, effort, estimated_kloc=None):
        """
        Calculate development time based on effort
        Uses standard COCOMO II formula
        
        :param effort: Estimated effort in person-months
        :param estimated_kloc: Optional estimated thousands of lines of code (not used in this version)
        :return: Development time in months
        """
        # COCOMO II development time calculation
        B = 0.91 + 0.01 * len(self.cost_driver_order)
        development_time = B * (effort ** 0.28)
        
        return float(development_time)  # Ensure it's a standard Python float