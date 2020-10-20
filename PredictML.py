import numpy as np
import pickle

def Run(filename, featureString):
    
    # Create numpy array from featureString and set the type to floats
    features = np.asarray(featureString.split(",")).astype(float)
    
    # Load the model from the modelfile
    loaded_model = pickle.load(open(filename, 'rb'))
    
    # Get the prediction number and return it to be displayed
    prediction = loaded_model.predict([features])
    return prediction