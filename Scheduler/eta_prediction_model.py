import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_data(file_path: str) -> pd.DataFrame:
    try:
        data = pd.read_csv(file_path)
        logger.info("Data loaded successfully.")
        return data
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise


def preprocess_data(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    try:
        # Feature engineering
        data["datetime"] = pd.to_datetime(data["date"] + " " + data["time"])
        data["day_of_week"] = data["datetime"].dt.weekday  # Monday = 0, Sunday = 6
        data["day_of_year"] = data["datetime"].dt.dayofyear
        data["hour"] = data["datetime"].dt.hour
        data.drop(columns=["date", "time", "datetime"], inplace=True)

        # Encode categorical variables
        label_encoder = LabelEncoder()
        data["route_id"] = label_encoder.fit_transform(data["route_id"])

        # Normalize numerical features
        scaler = StandardScaler()
        numeric_features = ["day_of_week", "day_of_year", "hour"]
        data[numeric_features] = scaler.fit_transform(data[numeric_features])

        # Split into features and target
        X = data.drop(columns=["eta"])
        y = data["eta"]

        logger.info("Data preprocessing completed.")
        return X, y
    except Exception as e:
        logger.error(f"Error during preprocessing: {e}")
        raise


def build_model(input_shape: int) -> keras.Model:
    try:
        model = keras.Sequential([
            layers.Input(shape=(input_shape,)),
            layers.Dense(64, activation='relu'),
            layers.Dense(32, activation='relu'),
            layers.Dense(1)  # Output layer for regression
        ])

        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        logger.info("Model built and compiled.")
        return model
    except Exception as e:
        logger.error(f"Error building model: {e}")
        raise


def train_model(model: keras.Model, X: pd.DataFrame, y: pd.Series, epochs: int = 50, batch_size: int = 16) -> keras.Model:
    try:
        # Split data into training and validation sets
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
                                                                #20% of the data is used for validation

        # Train the model
        history = model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            verbose=1
        )

        logger.info("Model training completed.")
        return model
    except Exception as e:
        logger.error(f"Error during training: {e}")
        raise


def save_model(model: keras.Model, file_path: str) -> None:
    try:
        model.save(file_path)
        logger.info(f"Model saved to {file_path}.")
    except Exception as e:
        logger.error(f"Error saving model: {e}")
        raise


def main():
    try:
        # Load data
        data = load_data("eta_dataset.csv")

        # Preprocess data
        X, y = preprocess_data(data)

        # Build the model
        model = build_model(input_shape=X.shape[1])

        # Train the model
        trained_model = train_model(model, X, y)

        # Save the trained model
        save_model(trained_model, "eta_prediction_model.h5")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")


if __name__ == "__main__":
    main()

