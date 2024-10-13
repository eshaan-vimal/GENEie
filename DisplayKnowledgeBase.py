import pickle


try:
    with open("KnowledgeBase.pkl", "rb") as file:
        KB = pickle.load(file)

except pickle.UnpicklingError as e:
    print(str(e))


for part in KB:
    print(part)
    print()