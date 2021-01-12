# Write a program to demonstrate the working of the decision tree based ID3 algorithm.
# Use an appropriate data set for building the decision tree and apply this
# knowledge to classify a new sample

import csv
import math
import random


# Majority Function which tells which class has more entries in given data-set
def majorClass(attributes, data, target):
    freq = {}
    index = attributes.index(target)
    for tuple in data:
        if tuple[index] in freq:
            freq[tuple[index]] += 1
        else:
            freq[tuple[index]] = 1
    max = 0
    major = ""
    for key in freq.keys():
        if freq[key]>max:
            max = freq[key]
            major = key
    return major


# Calculates the entropy of the data given the target attribute
def entropy(attributes, data, targetAttr):
    freq = {}
    dataEntropy = 0.0
    i = 0

    for entry in attributes:
        if (targetAttr == entry):
            break
        i = i + 1
    i = i - 1

    for entry in data:
        if entry[i] in freq:
            freq[entry[i]] += 1.0
        else:
            freq[entry[i]]  = 1.0
    #print(f"{targetAttr}: {freq}")

    for freq in freq.values():
       # dataEntropy += (-freq/14) * math.log(freq/14, 2)
        dataEntropy += (-freq/len(data)) * math.log(freq/len(data), 2)
        #print(dataEntropy)
    return dataEntropy


# Calculates the information gain (reduction in entropy) in the data when a particular attribute is chosen for splitting the data.
def info_gain(attributes, data, attr, targetAttr):
    freq = {}
    subsetEntropy = 0.0
    i = attributes.index(attr)

    for entry in data:
        if entry[i] in freq:
            freq[entry[i]] += 1.0
        else:
            freq[entry[i]]  = 1.0

    for val in freq.keys():
        valProb        = freq[val] / sum(freq.values())
        dataSubset     = [entry for entry in data if entry[i] == val]
        subsetEntropy += valProb * entropy(attributes, dataSubset, targetAttr)
    # print(subsetEntropy)
    # print(f"Target Entropy {targetAttr}")
    # print(entropy(attributes, data, targetAttr))
    S=entropy(attributes, data, targetAttr) - subsetEntropy
    # print(f"{attr}  {S}")
    #print("\n")
    return (S)


# This function chooses the attribute among the remaining attributes which has the maximum information gain.
def attr_choose(data, attributes, target):
    best = attributes[0]
    maxGain = 0;

    for attr in attributes:
        newGain = info_gain(attributes, data, attr, target)
        if newGain>maxGain:
            maxGain = newGain
            best = attr

    print(f"best:{best}")
    return best


# This function will get unique values for that particular attribute from the given data
def get_values(data, attributes, attr):
    index = attributes.index(attr)
    values = []

    for entry in data:
        if entry[index] not in values:
            values.append(entry[index])

    return values


# This function will get all the rows of the data where the chosen "best" attribute has a value "val"
def get_data(data, attributes, best, val):
    new_data = [[]]
    index = attributes.index(best)

    for entry in data:
        if (entry[index] == val):
            newEntry = []
            for i in range(0,len(entry)):
                if(i != index):
                    newEntry.append(entry[i])
            new_data.append(newEntry)

    new_data.remove([])
    return new_data


# This function is used to build the decision tree using the given data, attributes and the target attributes. It returns the decision tree in the end.
def build_tree(data, attributes, target):

    data = data[:]
    vals = [record[attributes.index(target)] for record in data]
    default = majorClass(attributes, data, target)

    if not data or (len(attributes) - 1) <= 0:
        return default
    elif vals.count(vals[0]) == len(vals):
        return vals[0]
    else:
        best = attr_choose(data, attributes, target)
        tree = {best:{}}
        print(f"tree{tree}")
        for val in get_values(data, attributes, best):
            print(f"val:{val}")
            new_data = get_data(data, attributes, best, val)
            print(f"newdata:{new_data}")
            newAttr = attributes[:]
            newAttr.remove(best)
            subtree = build_tree(new_data, newAttr, target)
            tree[best][val] = subtree
            #print("\n")
            #print(tree[best][val])
    return tree

#Main function
def execute_decision_tree():
    data = []
    #load file
    with open("3weather.csv") as tsv:
        for line in csv.reader(tsv):
            data.append(tuple(line))
        print("Number of records:",len(data))

        #set attributes
        attributes=['outlook','temperature','humidity','wind','play']
        target = attributes[-1]

        #set training data
        acc = []
        training_set = [x for i, x in enumerate(data)]
        tree = build_tree( training_set, attributes, target )
        print("\n")
        print(tree)
        print("\n")

        #execute algorithm on test data
        results = []
        test_set = [('overcast','mild','high','strong')]
        for entry in test_set:
            # print(f"entry:{entry}")
            tempDict = tree.copy()
            #print(tempDict)
            result = ""
            while(isinstance(tempDict, dict)):
                child=[]
                nodeVal=next(iter(tempDict))       # Get node names
                # print(f"nodeval:{nodeVal}")
                child=tempDict[next(iter(tempDict))].keys() #Get attr values
                # print(f"child: {child}")
                tempDict = tempDict[next(iter(tempDict))] # Get the subtree under the node
                # print(f"tempdict:{tempDict}")
                index = attributes.index(nodeVal)  # Get the index of node
                # print(index)
                value = entry[index]  # Get the value from test set at index
                # print(f"value:{value}")

                if(value in tempDict.keys()):    # If test value present in subtree
                    result = tempDict[value]
                    print("Yes")
                    print(f"result={result}")
                    tempDict = tempDict[value]
                    print(f"tempdict:{tempDict}")

                else:
                    print("No")
                    result = "Null" # When even value is not matching then break
                    break

            if result != "Null":
                results.append(result == entry[-1])
        print(result)


if __name__ == "__main__":
    execute_decision_tree()
