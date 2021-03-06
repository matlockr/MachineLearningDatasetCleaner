# This program will take a file specified by the user and clean the data
# to be used in a machine learning model.

# Imports
import numpy as np
import os

def isDigit(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

# Take a data array and convert it to pure float array
def CleanDataToFloats(isString, data):
    
    deleteInstances = []
    cleanData = np.array([])
    
    # stringTypes used to place indecies into the clean data where the string
    # of non-clean data exist
    stringTypes = []
    
    # For if the non-clean data is string based
    if isString:
        for x in range(len(data)):
            
            # Check if the element is null or non existant
            if isinstance(data[x], str):
                if str(data[x]) not in stringTypes:
                    stringTypes.append(str(data[x]))
                
                cleanData = np.append(cleanData, stringTypes.index(data[x]))
            else:
                deleteInstances.append(x)
                cleanData = np.append(cleanData, 0.00)
                
    # For if the non-clean data is number based
    else:
        stringTypes = ["Numeric"]
        for x in range(len(data)):
            # Check if the element is null or non existant
            if isDigit(data[x]):
                cleanData = np.append(cleanData, float(data[x]))
            else:
                deleteInstances.append(x)
                cleanData = np.append(cleanData, 0.00)
    
    return cleanData, deleteInstances, stringTypes

def InstancesToDeleteComparison(compareToList, newList):
    if len(newList) > 0:
            for i in range(len(newList)):
                if newList[i] not in compareToList:
                    compareToList.append(newList[i])
    return compareToList

def Run(filename, seperator, isRegression):
    
    # Get file from user
    userFile = open(filename, "r")
    
    # Starter list of all instances of the data file
    instanceList = []
    instanceCount = 0
    featureCount = 0        
    
    # put all instances in data file line by line into instanceList[]    
    for instance in userFile:
        tempStr = instance
        instanceCount += 1
        
        # Be sure to seperate the entries by commas
        for entry in tempStr.split(seperator):
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
    
    dataFullTranspose = dataFull.T
    dataFullClean = np.array([])

    instancesToDelete = []
    stringTypesArray = []
    
    # Start cleaning process for each of the features
    if isRegression:
        for x in range(featureCount):
            tmpFeatureString = "Feature " + str(x) + ": "
            stringTypesArray.append(tmpFeatureString)

            if isDigit(dataFull[0][x]): cleanFeature, deleteInstance, stringTypes = CleanDataToFloats(False, dataFullTranspose[x])
            else: cleanFeature, deleteInstance, stringTypes = CleanDataToFloats(True, dataFullTranspose[x])
            
            dataFullClean = np.append(dataFullClean, cleanFeature)   
            stringTypesArray.append(stringTypes)
        
        instancesToDelete = InstancesToDeleteComparison(instancesToDelete, deleteInstance)
    else:
        for x in range(featureCount-1):
            tmpFeatureString = "Feature " + str(x) + ": "
            stringTypesArray.append(tmpFeatureString)

            if isDigit(dataFull[0][x]):cleanFeature, deleteInstance, stringTypes = CleanDataToFloats(False, dataFullTranspose[x])
            else:cleanFeature, deleteInstance, stringTypes = CleanDataToFloats(True, dataFullTranspose[x])

            dataFullClean = np.append(dataFullClean, cleanFeature)   
            stringTypesArray.append(stringTypes)
            
        instancesToDelete = InstancesToDeleteComparison(instancesToDelete, deleteInstance)
                    
        # Do the cleaning for the target value
        targetInstanceDelete = []
        for x in range(instanceCount):
            if isDigit(dataFullTranspose[featureCount-1][x]):
                dataFullClean = np.append(dataFullTranspose, dataFullTranspose[featureCount-1][x])
            else:
                if isinstance(dataFullTranspose[featureCount-1][x], str):
                    if str(dataFullTranspose[featureCount-1][x]).lower() == "no":
                        dataFullClean = np.append(dataFullClean, 0)
                    elif str(dataFullTranspose[featureCount-1][x]).lower() == "yes":
                        dataFullClean = np.append(dataFullClean, 1)
                    else:
                        dataFullClean = np.append(dataFullClean, 999)
                        targetInstanceDelete.append(x)
        
        instancesToDelete = InstancesToDeleteComparison(instancesToDelete, targetInstanceDelete)
        
    # Reshape and set presicion on new array
    dataFullClean = dataFullClean.reshape(featureCount, instanceCount).T
    np.set_printoptions(suppress=True)

    # Delete instances of bad or missing data
    for i in range(len(instancesToDelete)):
        dataFullClean = np.delete(dataFullClean, instancesToDelete[i], 0)
        instanceCount -= 1
        for j in range(len(instancesToDelete)):
            instancesToDelete[j] -= 1    
                 
    # Make new file for clean data
    tmpFileName, file_exe = os.path.splitext(filename)
    newFilePath = tmpFileName + "CLEAN" + file_exe
    newFile = open(newFilePath, 'w')
    
    # Put clean data into new file
    for x in range(instanceCount):
        writeString = ""
        for entry in range(featureCount-1):
            writeString += str(dataFullClean[x][entry]) + ","
        writeString += str(dataFullClean[x][featureCount-1]) + "\n"
        newFile.write(writeString)
    
    # Setup new file for putting string types into
    stringTypesFileName = tmpFileName + "FeatureTypes" + file_exe
    stringTypesFile = open(stringTypesFileName, 'w')
    
    # Put the string type into the new file
    tmpString = ""
    stringTypesArray.append("Feature")
    for x in range(len(stringTypesArray)):
        if "Feature" in stringTypesArray[x]:
            tmpString += "\n"
            stringTypesFile.write(tmpString)
            tmpString = ""
            tmpString = str(stringTypesArray[x])
        else:
            tmpString = tmpString + ", " + str(stringTypesArray[x])
    
    writeString = "\nFeature: " + str(featureCount) + "\nInstances: " + str(instanceCount)
    stringTypesFile.write(writeString)
    
    # Close the writing file
    newFile.close()
    stringTypesFile.close()