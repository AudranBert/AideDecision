import csv
import AideDecision.vote as vote

def load_csv(filename):
    with open(filename, "r") as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
        votes = [[] for i in range(len(data[0]))]
        for pref in data:
            for i, vote in enumerate(pref):
                votes[i].append(vote)
    return votes

if __name__ == "__main__":
    data = load_csv("profil1.csv")   
    print(data)