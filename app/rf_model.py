#load packages
import pandas as pd
import numpy as np
import datetime
import shap 
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from process import Preprocessor



class RunRandomForest():
    def __init__(self, data, target: str, exclude_cols = None):
        self.data = data.dropna(subset=[target])
        self.target = target 
        if self.target == 'Carry':
            self.target_corr = ['rawCarryGame', 'TotalDistance']
        elif self.target == 'TotalDistance':
            self.target_corr = ['rawCarryGame', 'Carry']
        default =  ['Date', self.target] + self.target_corr

        if exclude_cols is None:
            self.exclude_cols = default
        # else:
        #     self.exclude_cols = list(set(exclude_cols + default))
        self.X = self.data.drop(columns=self.exclude_cols)#drop response and date var
        self.y = self.data[target].values 

        #Drop rows with NaNs in any feature
        tmp = self.X.copy()
        tmp['target'] = self.y
        tmp = tmp.dropna()
        self.y = tmp['target'].values
        self.X = tmp.drop(columns=['target'])
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
    

    def fit(self, cv, log_cv = False): 
        base_rf = RandomForestRegressor(oob_score=True, random_state=42)
        self.param_grid = {
            'n_estimators': [50, 100],                   
            'max_depth': [None, 5, 10],                   
            'min_samples_split': [2, 5],                
            'min_samples_leaf': [1, 2],                    
            'max_features': ['sqrt', 0.5],       
            'bootstrap': [True]                      
        }

        self.grid_search = GridSearchCV(base_rf, param_grid=self.param_grid,scoring='neg_mean_squared_error', cv= cv, n_jobs=-1)
        self.grid_search.fit(self.X_train, self.y_train)
        if log_cv:
            cv_results = pd.DataFrame(self.grid_search.cv_results_)
            cv_sorted = cv_results.sort_values(by = 'mean_test_score', ascending= False)
            print("CV Results:", cv_sorted.head())
            today = datetime.now().date()
            cv_sorted.to_csv(f"cv_results_{today}.csv", index = False)
        self.tuned_rf = self.grid_search.best_estimator_
        print(self.tuned_rf)
        self.y_pred =  self.tuned_rf.predict(self.X_test)
        return self.tuned_rf
    
    
    def evaluate(self):
        if not hasattr(self, 'tuned_rf'):
            raise AttributeError("Model has not been fit. Call fit_tune() first.")

        model = self.tuned_rf
        self.oob = model.oob_score_
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
    
    def shap_values(self):
        if not hasattr(self, 'tuned_rf'):
            raise ValueError("Model has not been tuned yet. Call .tune() first.")
        explainer = shap.TreeExplainer(self.tuned_rf)
        shap_values = explainer.shap_values(self.X_test)
        return shap_values#, shap.summary_plot(shap_values, self.X_test)



###### PERFORM RANDOM FOREST REGRESSION ########
# data = Preprocessor().get_data() #load data 
# target = 'Carry'

# reg = RunRandomForest(data, target= target)
# reg.onehotencode()
# reg.split_data(size = 0.3)
# reg.fit(cv=5)
# oob, mse, r2 = reg.evaluate()
# feat_imp = reg.feature_importance(top_n=10)
# shap_vals = reg.shap_values()

# print(feat_imp)
# print(f"OOB Score: {oob:.3f}")
# print(f"Mean Squared Error: {mse:.2f}")
# print(f"R² Score: {r2:.3f}")
# print(f"SHAP values: {shap_vals}")















        