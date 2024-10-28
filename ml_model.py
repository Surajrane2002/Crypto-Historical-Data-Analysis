import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def train_model(data):
    """
    Train the model on input features to predict future price differences.
    Args:
        data (DataFrame): Historical data with calculated metrics.
    Returns:
        model (LinearRegression): Trained model.
        accuracy (float): Model accuracy (R^2 score).
    """
    features = [
        "Days_Since_High_Last_7_Days",
        "%_Diff_From_High_Last_7_Days",
        "Days_Since_Low_Last_7_Days",
        "%_Diff_From_Low_Last_7_Days"
    ]
    X = data[features]
    y = data[["%_Diff_From_High_Next_5_Days", "%_Diff_From_Low_Next_5_Days"]]
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Model accuracy
    accuracy = model.score(X_test, y_test)
    print("Model Accuracy:", accuracy)
    return model, accuracy

def predict_outcomes(model, input_data):
    """
    Use the trained model to predict outcomes based on new input data.
    Args:
        model: Trained machine learning model.
        input_data (DataFrame): New input data for predictions.
    Returns:
        predictions (DataFrame): Predicted values.
    """
    predictions = model.predict(input_data)
    return pd.DataFrame(predictions, columns=["Predicted_%Diff_From_High", "Predicted_%Diff_From_Low"])

# Example usage
if __name__ == "__main__":
    # Load data for model training
    data = pd.read_excel("crypto_data.xlsx")
    model, accuracy = train_model(data)
    
    # Sample prediction input
    sample_input = data[
        ["Days_Since_High_Last_7_Days", "%_Diff_From_High_Last_7_Days", 
         "Days_Since_Low_Last_7_Days", "%_Diff_From_Low_Last_7_Days"]
    ].iloc[:5]
    
    predictions = predict_outcomes(model, sample_input)
    print("Predictions:\n", predictions)
