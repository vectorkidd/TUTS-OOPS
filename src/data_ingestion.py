import pandas as pd
import os
from sklearn.model_selection import train_test_split
import logging
import yaml

log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

#logging configuration
logger = logging.getLogger('data_ingestion_logger')
logger.setLevel('DEBUG')

console_handler = logging.StreamHandler()
console_handler.setLevel('DEBUG')

file_handler = logging.FileHandler(os.path.join(log_dir, 'data_ingestion.log'))
file_handler.setLevel('DEBUG')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

def load_params(params_path: str) -> dict:
    """Load parameters from a YAML file."""
    try:
        with open(params_path, 'r') as file:
            params = yaml.safe_load(file)
            logger.info(f"Parameters loaded successfully from {params_path}")
            return params
    except yaml.YAMLError as e:
        logger.error(f"Error loading YAML file: {e}")
        raise
    except Exception as e:
        logger.error(f"Error loading parameters: {e}")
        raise

def load_data(data_url: str) -> pd.DataFrame:
    """Load data from a CSV file."""
    try:
        df = pd.read_csv(data_url)
        logger.info(f"Data loaded successfully from {data_url}")
        return df
    except pd.errors.ParserError as e:
        logger.error(f"Error parsing CSV file: {e}")
        raise
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the data by handling missing values."""
    try:
        initial_shape = df.shape
        df.drop(columns=['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], inplace=True)
        df.rename(columns = {'v1': 'target', 'v2': 'text'}, inplace = True)
        final_shape = df.shape
        logger.debug(f"Preprocessed data: dropped rows with missing values. "
                    f"Initial shape: {initial_shape}, Final shape: {final_shape}")
        return df
    except KeyError as e:
        logger.error(f"Missing column in the dataframe: {e}")
        raise
    except Exception as e:
        logger.error(f"Error during preprocessing: {e}")
        raise

def save_data(train_data: pd.DataFrame, test_data: pd.DataFrame, data_path: str) -> None:
    """Save the train and test data to CSV files."""
    try:
        raw_data_path = os.path.join(data_path, 'raw')
        os.makedirs(raw_data_path, exist_ok=True)
        train_file_path = os.path.join(raw_data_path, 'train.csv')
        test_file_path = os.path.join(raw_data_path, 'test.csv')
        
        train_data.to_csv(train_file_path, index=False)
        test_data.to_csv(test_file_path, index=False)
        
        logger.info(f"Train data saved to {train_file_path}")
        logger.info(f"Test data saved to {test_file_path}")
    except Exception as e:
        logger.error(f"Error saving data: {e}")
        raise

def main():
    try:
        params = load_params(params_path='params.yaml')
        test_size = params['data_ingestion']['test_size']
        random_state = params['data_ingestion']['random_state']
        
        data_path = 'https://raw.githubusercontent.com/vectorkidd/TUTS-OOPS/refs/heads/main/experiments/spam.csv'
        df = load_data(data_url=data_path)
        final_df = preprocess_data(df)  
        train_data, test_data = train_test_split(final_df, test_size=test_size, random_state=random_state)
        save_data(train_data, test_data, data_path='./data')
        logger.info("Data ingestion completed successfully.")
    except Exception as e:
        logger.error(f"Data ingestion failed: {e}")
        raise

if __name__ == "__main__":
    main()  