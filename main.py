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
    elif isinstance(vote_results, list):
        for i in vote_results:
            print(i)
    else:
        print(vote_results)

def print_dict(vote_results):
    for i in vote_results:
        print(i,":", vote_results[i])

def print_condat(winners):
    place = 1
    current = -1
    if winners[0][1] == winners[1][1]:
        print("Il n'y a pas de vainqueur selon la méthode de Condorcet")
    for winner in winners:
        print(f"Le candidat {winner[0]} a gagné {winner[1]} points, il est {place}ème")
        if current != winner[1]:
            place+=1
            current = winner[1]

def print_coombs(dico):
    tour = 1
    winner = None
    print("Nous comptons le nombre de dernières places pour chaque candidat")
    for turn in dico.values():
        print(f"Le candidat éliminé au tour {tour} est {turn[0][0]}")
        tour+=1
    print(f"Le gagnant du vote Coombs est {turn[-1][0]}")

if __name__ == "__main__":
    voters = load_csv("data/social/profil1.csv")   
    print()
    vote.one_turn_vote(voters)
    print()
    vote.two_turn_vote(voters)
    print()
    vote.alternative_vote(voters)
    print()
    print_coombs(vote.coombs(voters))
    print()
    winner_con, score = vote.condorcet(voters)
    print_condat(winner_con)
    print()
    winners = vote.borda(voters)
    print_condat(winners)
    print()
    vote.copeland(voters)
    print()
    vote.schulze(voters)
