#load packages
import pandas as pd
import numpy as np
import numbers
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from process import Preprocessor 


class RandomForest():
    def __init__(self, data, target: str):
        self.data = data.dropna(subset=[target])
        self.exclude_cols = ['Date', target]
        self.X = self.data.drop(columns=self.exclude_cols)#drop response and date var
        self.y = self.data[target].values 
        assert np.issubdtype(self.y.dtype, np.number), "Y must be numeric"
    
    def onehotencode(self):
        ''' One hot encodes categorical columns of X. Modifies X in place. Does not return anything'''

        self.X = self.X.copy()
        self.x_cat = self.X.select_dtypes(include=['object']).columns
        if len(self.x_cat) > 0:
            self.X = pd.get_dummies(data=self.X, columns= self.x_cat)
        else:
            self.X = self.X
        
  
    def split_data(self, size = 0.3):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size= size, random_state=42)
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def fit(self, n_estimators = 10):
        self.rf = RandomForestRegressor(n_estimators=n_estimators, random_state=42, oob_score=True)
        self.rf.fit(self.X_train, self.y_train)
    
    def tune(self, n): #n = number of cv 
        self.param_grid = {
            'n_estimators': [50, 100, 200],                   
            'max_depth': [None, 5, 10, 20],                   
            'min_samples_split': [2, 5, 10],                
            'min_samples_leaf': [1, 2, 4],                    
            'max_features': ['sqrt', 0.5],       
            'bootstrap': [True]                      
        }

        self.grid_search = GridSearchCV(self.rf, param_grid=self.param_grid,scoring='neg_mean_squared_error', cv= n, n_jobs=-1)
        self.grid_search.fit(self.X_train, self.y_train)
        self.tuned_rf = self.grid_search.best_estimator_
        return self.tuned_rf
    
    def predict(self):
        #use tuned model if called, otherwise use base
        model = getattr(self, 'tuned_rf', None)
        if model is None:
            if not hasattr(self, 'rf'):
                raise AttributeError("Model has not been fit. Call .fit() or .tune() first.")
            model = self.rf

        self.y_pred = model.predict(self.X_test)
        return self.y_pred

    
    def evaluate(self):
        model = getattr(self, 'tuned_rf', None)
        if model is None:
            if not hasattr(self, 'rf'):
                raise AttributeError("Model has not been fit. Call .fit() or .tune() first.")
        model = self.rf
        self.oob = self.tuned_rf.oob_score_
        self.mse = mean_squared_error(self.y_test, self.y_pred)
        self.r2 = r2_score(self.y_test, self.y_pred)
        return self.oob, self.mse, self.r2
    
    def feature_importance(self, top_n: int = 10):
        imp_model = getattr(self, 'tuned_rf', getattr(self, 'rf', None))
        if imp_model is None or not hasattr(imp_model, 'feature_importances_'):
            raise AttributeError("Model must be fit or tuned before checking feature importances.")
        
        imp = imp_model.feature_importances_
        x_names = self.X.columns  # Already one-hot encoded
        feat_df = pd.DataFrame({'Feature': x_names, 'Importance': imp})
        feat_df = feat_df.sort_values(by='Importance', ascending=False)

        return feat_df.head(top_n)

###### PERFORM RANDOM FOREST REGRESSION ########
data = Preprocessor().get_data() #load data 
target = 'Carry'

reg = RandomForest(data, target)
reg.onehotencode()
reg.split_data(size = 0.3)
reg.fit(n_estimators= 100)
reg.tune(n=5)
reg.predict()
oob, mse, r2 = reg.evaluate()
feat_imp = reg.feature_importance(top_n=10)

print(feat_imp)
print(f"OOB Score: {oob:.3f}")
print(f"Mean Squared Error: {mse:.2f}")
print(f"R² Score: {r2:.3f}")














        