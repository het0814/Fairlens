import pandas as pd
import numpy as np  
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.arima.model import ARIMA
import os

def load_local_company_data():
    csv_path = os.path.join("app", "Dashboard_Pages", "data", "data.csv")
    df = pd.read_csv(csv_path)
    return df

def get_predicted_attrition_by_years(forecast_years=5):
    df = load_local_company_data().copy()

    if 'Attrition' not in df.columns:
        raise ValueError("Column 'Attrition' is missing from the dataset.")
    
    df['Attrition'] = df['Attrition'].apply(lambda x: 1 if x == 'Yes' else 0)
    df = pd.get_dummies(df, columns=['Department', 'OverTime'], drop_first=True)

    features = ['Age', 'YearsAtCompany', 'JobSatisfaction',
                'WorkLifeBalance', 'PerformanceRating', 'PayRate']
    features += [col for col in df.columns if col.startswith(('Department_', 'OverTime_'))]

    if not all(feature in df.columns for feature in features):
        raise ValueError("Some required features are missing in the dataset.")

    X = df[features]
    y = df['Attrition']

    # ML model just for learning attrition patterns
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    xgb_model = XGBClassifier(random_state=42, eval_metric='logloss')
    xgb_model.fit(X_train, y_train)
    y_pred = xgb_model.predict(X_test)

    X_test_with_predictions = X_test.copy()
    X_test_with_predictions['Predicted_Attrition'] = y_pred

    # Aggregate by 'YearsAtCompany' to create a time series
    ts = X_test_with_predictions.groupby('YearsAtCompany')['Predicted_Attrition'].mean().sort_index()

    # Fit ARIMA model to forecast attrition
    model = ARIMA(ts, order=(1, 1, 1))  # You can tune these params
    fitted_model = model.fit()

    forecast = fitted_model.forecast(steps=forecast_years)
    forecast.index = range(ts.index.max() + 1, ts.index.max() + 1 + forecast_years)

    # Combine historical + forecast
    full_series = pd.concat([ts, forecast])
    full_series.name = 'Attrition_Forecast'

    return full_series

def get_gender_diversity_predictions(forecast_years=5): 
    df = load_local_company_data().copy()

    if 'DateofHire' not in df.columns or 'Sex' not in df.columns:
        raise ValueError("Required columns 'DateofHire' or 'Sex' are missing.")
    
    df['DateofHire'] = pd.to_datetime(df['DateofHire'])
    df['Year'] = df['DateofHire'].dt.year

    gender_categories = ['Female', 'Male', 'Transgender', 'Non-binary/non-conforming',
                         'Prefer not to say', 'Other']
    sanitized_gender_categories = [category.replace(" ", "_").replace("/", "_").replace("-", "_") for category in gender_categories]

    for category, sanitized in zip(gender_categories, sanitized_gender_categories):
        df[f'Is{sanitized}'] = df['Sex'].apply(lambda x: 1 if x == category else 0)

    gender_trends = df.groupby('Year').agg({
        f'Is{sanitized}': 'mean' for sanitized in sanitized_gender_categories
    } | {'Sex': 'count'}).reset_index()
    gender_trends.rename(columns={'Sex': 'TotalHires'}, inplace=True)

    predictions = {}

    for gender in [f'Is{sanitized}' for sanitized in sanitized_gender_categories]:
        ts = gender_trends.set_index('Year')[gender]
        ts.index = pd.PeriodIndex(ts.index, freq='Y')  # ✅ convert index to PeriodIndex

        try:
            model = ARIMA(ts, order=(1, 1, 1))
            fitted_model = model.fit()
            forecast = fitted_model.forecast(steps=forecast_years)
            forecast.index = pd.period_range(start=ts.index[-1] + 1, periods=forecast_years, freq='Y')
            predictions[gender] = forecast
        except Exception as e:
            print(f"ARIMA model failed for {gender}: {e}")
            fallback_index = pd.period_range(start=ts.index[-1] + 1, periods=forecast_years, freq='Y')
            predictions[gender] = pd.Series([None] * forecast_years, index=fallback_index)

    return gender_trends, predictions
   
def get_diversity_predictions():
    df = load_local_company_data().copy()

    df['DateofHire'] = pd.to_datetime(df['DateofHire'])
    df['Year'] = df['DateofHire'].dt.year

    diversity_attributes = ['Indigenous', 'Disability', 'Minority', 'Veteran']
    for attr in diversity_attributes:
        df[attr] = df[attr].apply(lambda x: 1 if x == 'Yes' else 0)

    df = pd.get_dummies(df, columns=['RecruitmentSource', 'Department'], drop_first=True)

    label_encoder = LabelEncoder()
    non_numeric_columns = df.select_dtypes(include=['object']).columns
    for column in non_numeric_columns:
        df[column] = label_encoder.fit_transform(df[column].astype(str))

    diversity_trends = df.groupby('Year').agg({
        'Indigenous': 'mean',
        'Disability': 'mean',
        'Minority': 'mean',
        'Veteran': 'mean',
        'Ethnicity': 'count', 
        'PayRate': 'mean',
        'JobInvolvement': 'mean',
        'JobSatisfaction': 'mean',
        'WorkLifeBalance': 'mean',
        'YearsAtCompany': 'mean',
        'OverTime': 'mean'
    }).reset_index()

    diversity_trends.rename(columns={'Ethnicity': 'TotalHires'}, inplace=True)

    features = ['Year', 'TotalHires', 'PayRate', 'JobInvolvement', 'JobSatisfaction',
                'WorkLifeBalance', 'YearsAtCompany', 'OverTime']
    targets = ['Indigenous', 'Disability', 'Minority', 'Veteran']

    future_data = []

    for target in targets:
        X = diversity_trends[features]
        y = diversity_trends[target]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        rf = RandomForestRegressor(random_state=42, n_estimators=100)
        rf.fit(X_train, y_train)
        future_years = pd.DataFrame({
            'Year': [year for year in range(diversity_trends['Year'].max() + 1, diversity_trends['Year'].max() + 11)],
            'TotalHires': [diversity_trends['TotalHires'].mean() * (1 + 0.05) ** (i + 1) for i in range(10)],           
            'PayRate': [diversity_trends['PayRate'].mean() * (1 + 0.03 * (i + 1)) + np.random.uniform(-0.5, 0.5) for i in range(10)],   
            'JobInvolvement': [diversity_trends['JobInvolvement'].mean()] * 10, 
            'JobSatisfaction': [diversity_trends['JobSatisfaction'].mean() + (i * 0.02) + np.random.uniform(-0.01, 0.01) for i in range(10)],
            'WorkLifeBalance': [diversity_trends['WorkLifeBalance'].mean() + (i * 0.01) + np.random.uniform(-0.005, 0.005) for i in range(10)],
            'YearsAtCompany': [diversity_trends['YearsAtCompany'].mean() + (i * 0.1) for i in range(10)],
            'OverTime': [diversity_trends['OverTime'].mean() + ((-1) ** i) * 0.02 for i in range(10)]
        })
        future_years[target] = rf.predict(future_years[features])
        future_data.append(future_years[['Year', target]])
    all_data = pd.concat([diversity_trends[['Year'] + targets]] + future_data)

    return all_data

def get_preformance_predictions():
    df = load_local_company_data().copy()
    features = ['YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion', 
                'JobSatisfaction', 'JobInvolvement', 'WorkLifeBalance', 
                'PayRate', 'PercentSalaryHike']
    target = 'PerformanceRating'

    X = df[features]  
    y = df[target]   

    X = X.fillna(X.median())

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    svr_model = SVR(kernel='rbf')  
    svr_model.fit(X_train, y_train)

    y_pred = svr_model.predict(X_test)
    return y_pred

