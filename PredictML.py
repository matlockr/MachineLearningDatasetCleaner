import numpy as np
import pickle

def Run(filename, featureString):
    
    features = np.asarray(featureString.split(",")).astype(float)
    loaded_model = pickle.load(open(filename, 'rb'))
    prediction = loaded_model.predict([features])
    return prediction