from sklearn.linear_model import LinearRegression, LogisticRegression
import numpy as np

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
        dataFull[instance][featureCount-1] = dataFull[instance][featureCount-1].rstrip("\n").T
    
    #features = np.array(dataFull[])
    print(dataFull)