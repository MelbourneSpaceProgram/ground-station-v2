import pandas as pd
import numpy as np

class BatCurvInterp:

    def __init__(self, poly_order) -> None:
        self.orig_data_df = df = pd.read_csv('client/EPS/Battery Curve.csv')
        self.poly_order = poly_order
        self.poly = self.fit_poly(df['Cell Voltage (V)'], df['Battery Charge (%)'], poly_order)

    #fit the data to a polynomial equation
    def fit_poly(self, x, y, poly_order):
        return np.polyfit(x, y, poly_order)

    #Ensure the value to be interpolated is within the dataset upper and lower limits
    def check_limit(self, val):
        if val > min(self.orig_data_df['Cell Voltage (V)']) and val < max(self.orig_data_df['Cell Voltage (V)']):
            return True
        return False

    #Interpolate value into fitted polynomial equation
    def interp_val(self, val, mean=False):
        #Check if the val variable is a single value or a list
        if type(val) == list:
            _vals = []
            #Filter out values that exceed the limits
            for v in val:
                if self.check_limit(v):
                    _vals.append(v)
            val = _vals
        #Check if single input is within limits
        elif not self.check_limit(val):
            print("Value out of bounds!")
            return
        
        #Interpolate val
        interpolated_val = np.polyval(self.poly, val)

        #return mean of values if there more than one and mean has been set to true
        if mean:
            return np.mean(interpolated_val)
        return(interpolated_val)
            
