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


def print_result(vote_results):
    if isinstance(vote_results, dict):
        print_dict(vote_results)
    else:
        print(vote_results)

def print_dict(vote_results):
    for i in vote_results:
        print(i,":", vote_results[i])

if __name__ == "__main__":
    voters = load_csv("data/profil1.csv")   
    result = vote.two_turn_vote(voters)
    print_result(result)
