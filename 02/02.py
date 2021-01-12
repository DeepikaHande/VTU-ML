# For a given set of training data examples stored in a .CSV file, implement and
# demonstrate the Candidate-Elimination algorithmto output a description of the set
# of all hypotheses consistent with the training examples.

import numpy as np
import pandas as pd

# Loading Data from a CSV File
data = pd.DataFrame(data=pd.read_csv('2ce.csv'))

# Separating concept features from Target
concepts = data.iloc[:,0:-1].values
# print("\n\nCONCEPTS:")
# print("-------------------------------------------")
# print(concepts)
# print("-------------------------------------------")

# Isolating target into a separate DataFrame
target =data.iloc[:,-1].values
# print("\n\nTARGETS:")
# print("-------------------------------------------")
# print(target)
# print("-------------------------------------------\n\n")

def learn(concepts, target):
    specific_h = concepts[0].copy()
    general_h = [["?" for i in range(len(specific_h))] for i in range(len(specific_h))]

    # The learning iterations
    for i, h in enumerate(concepts):

        # Checking if the hypothesis has a positive target
        if target[i] == "Yes":
            for x in range(len(specific_h)):

                # Change values in S & G only if values change
                if h[x] != specific_h[x]:
                    specific_h[x] = '?'
                    general_h[x][x] = '?'

        # Checking if the hypothesis has a positive target
        if target[i] == "No":
            for x in range(len(specific_h)):
                # print(f"specific = {specific_h[x]}\n")
                # For negative hyposthesis change values only  in G
                if h[x] != specific_h[x]:
                    general_h[x][x] = specific_h[x]
                    #print(f"general{x}={general_h[x][x]}")
                else:
                    general_h[x][x] = '?'
    # find indices where we have empty rows, meaning those that are unchanged
    indices = [i for i,val in enumerate(general_h) if val == ['?', '?', '?', '?', '?', '?']]
    for i in indices:
        # remove those rows from general_h
        general_h.remove(['?', '?', '?', '?', '?', '?'])

    # Return final values
    return specific_h, general_h

s_final, g_final = learn(concepts, target)
print("Final S:", s_final, sep="\n")
# print("\n")
print("Final G:", g_final, sep="\n")
