# Implement and demonstratethe FIND-Salgorithm for finding the most specific hypothesis
# based on a given set of training data samples. Read the training data from a .CSV file.

import numpy as np
import pandas as pd

data = pd.read_csv('1finds.csv')
# print("\nDATASET:\n", data)

concepts=data.iloc[:,0:-1].values
# print("\n\nCONCEPTS:")
# print("-------------------------------------------")
# print(concepts)
# print("-------------------------------------------")

target = data.iloc[:,-1].values
# print("\n\nTARGETS:")
# print("-------------------------------------------")
# print(target)
# print("-------------------------------------------\n\n")

def train(concepts,target):
    count=0
    specific_h = concepts[0]
    for i,h in enumerate(concepts):
        print("Iteration: ", i)
        print(h)
        if target[i] == "Yes":
            for x in range(len(specific_h)):
                if h[x] == specific_h[x]:
                    pass
                else:
                    specific_h[x] = "?"
            count = count + 1
            print (f"Hypothesis after sample number:{count} processed: {specific_h} \n")
        else:
            count = count + 1
            print (f"Negative sample number:{count} Same Hypothesis: {specific_h} \n")

    return specific_h

specific_h = train(concepts,target)
