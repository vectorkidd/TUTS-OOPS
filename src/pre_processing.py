import os
import pandas as pd
import logging
from sklearn.preprocessing import LabelEncoder
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import nltk
import string
nltk.download('stopwords')
nltk.download('punkt_tab')

#logging configuration
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

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

def text_transform(text):
    """Transform text by lowering case, removing punctuation, stopwords, and stemming."""
    try:
        ps = PorterStemmer()
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = nltk.word_tokenize(text)
        text = [word for word in text if word.isalnum()]
        text = [word for word in text if word not in stopwords.words('english') and word not in string.punctuation]
        text = [ps.stem(word) for word in text]
        transformed_text = ' '.join(text)
        return transformed_text
    except Exception as e:
        logger.error(f"Error during text transformation: {e}")
        raise

def pre_process_df(df, text_column="text", target_column="target"):
    """Preprocess the dataframe by transforming text and encoding target labels."""
    try:
        logger.debug("Starting dataframe preprocessing.")
        # Transform text data
        le = LabelEncoder()
        df[target_column] = le.fit_transform(df[target_column])
        logger.debug("Target cplumn encoded successfully.")

        #remove duuplicates
        df.drop_duplicates(keep='first')
        logger.debug("Duplicates removed successfully.")

        df.loc[:, text_column] = df[text_column].apply(text_transform)
        logger.debug("Text column transformed successfully.")
        return df
    except KeyError as e:
        logger.error(f"Missing column in the dataframe: {e}")
        raise
    except Exception as e:
        logger.error(f"Error during dataframe preprocessing: {e}")
        raise

def main(text_column="text", target_column="target"):
    """Main function"""

    try:
        train_data=pd.read_csv('data/train.csv')
        test_data=pd.read_csv('data/test.csv')
        logger.info("Train and test data loaded successfully.")

        train_data = pre_process_df(train_data, text_column, target_column)
        test_data = pre_process_df(test_data, text_column, target_column)
        logger.info("Train and test data preprocessed successfully.")

        data_path = os.path.join("./data", "interim")
        os.makedirs(data_path, exist_ok=True)

        train_data.to_csv(os.path.join(data_path, 'train_processed.csv'), index=False)
        test_data.to_csv(os.path.join(data_path, 'test_processed.csv'), index=False)

        logger.debug("Processed train and test data saved successfully to." + data_path)

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        logger.error(f"Empty data error: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to complete data transformation: {e}")
        raise

if __name__ == "__main__":
    main()