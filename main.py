import csv
import vote

def load_csv(filename):
    with open(filename, "r") as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
        votes = [[] for i in range(len(data[0]))]
        for pref in data:
            for i, vote in enumerate(pref):
                votes[i].append(int(vote))
    return votes

if __name__ == "__main__":
    data = load_csv("profil1.csv")
    result = vote.get_votes_distribution(data)
    print(result)