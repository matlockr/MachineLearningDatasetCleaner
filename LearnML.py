from sklearn.linear_model import LinearRegression, LogisticRegression
import numpy as np
import pickle
import os

def Run(datasetFile):
    
    # Get file from user
    userFile = open(datasetFile, "r")
    
    # Starter list of all instances of the data file
    instanceList = []
    instanceCount = 0
    featureCount = 0        
    
    # put all instances in data file line by line into instanceList[]    
    for instance in userFile:
        tempStr = instance
        instanceCount += 1
        
        # Be sure to seperate the entries by commas
        for entry in tempStr.split(','):
            instanceList.append(entry)
            featureCount += 1
                
    # Close file
    userFile.close()
    
    # Adjust size of feature count
    featureCount = int(featureCount / instanceCount)
    
    # With data now seperated we can make the numpy array and transpose it    
    dataFull = np.asarray(instanceList).reshape(instanceCount * featureCount).reshape(instanceCount, featureCount)
    
    # Get rid of all the '\n' in array
    for instance in range(instanceCount):
        dataFull[instance][featureCount-1] = dataFull[instance][featureCount-1].rstrip("\n")
    
    features = np.array(dataFull.T[0:featureCount-1]).astype(float).reshape(featureCount-1, instanceCount).T
    target = np.array(dataFull.T[featureCount-1]).astype(float)
    
    # Setup Machine Learning
    isClassification = False
    for i in range(len(target)):
        if int(target[i]) == 0 or int(target[i]) == 1:
            isClassification = True
        else:
            isClassification = False
            break
        
    mlModel = None
    
    if isClassification:
        mlModel = LogisticRegression().fit(features, target)
    else:
        mlModel = LinearRegression().fit(features, target) 

    
    # Make new file for Model data
    tmpFileName, file_exe = os.path.splitext(datasetFile)
    newFilePath = tmpFileName + "MODEL" + ".sav"
    pickle.dump(mlModel, open(newFilePath, 'wb'))
     
    # load the model from disk
    # loaded_model = pickle.load(open(filename, 'rb'))
    # result = loaded_model.score(features, target)
    # print(result)