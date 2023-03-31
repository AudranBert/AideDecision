import numpy as np

def get_votes_distribution(voters, eliminated=[], reverse=False):
    candidates_number = len(voters[0])
    rank = 0 if not reverse else candidates_number-1
    distribution = [0 for i in range(candidates_number)]
    for pref in voters:
        current_choice = rank
        while pref[current_choice] in eliminated:
            current_choice = current_choice + 1 if not reverse else current_choice - 1
        distribution[pref[current_choice] - 1] += 1
    return distribution

def order_results(vote_distribution_results):
    results = []
    for i, votes in enumerate(vote_distribution_results):
        if votes>0:
            results.append((i+1, votes))
    return sorted(
        results, 
        key=lambda x: x[1],
        reverse=True
    )

def absolute_majority(result):
    total_voters = 0
    for votes in result:
        total_voters += votes
    majority = max(result)
    return majority / total_voters > 0.5

def one_turn_vote(voters):
    result = order_results(get_votes_distribution(voters))
    print(f"Le gagnant du vote au premier tour est {result[0][0]}")
    return result

def two_turn_vote(voters, candidates_number=2):
    nb_cand = len(voters[0])
    results = dict()
    turn_1 = one_turn_vote(voters)
    results[f'turn_1'] = turn_1
    eliminated = {i for i in range(1, nb_cand+1)}
    eliminated -= {turn_1[0][0], turn_1[1][0]}
    turn_2 =  order_results(get_votes_distribution(voters, eliminated))
    results[f'turn_2'] = turn_2
    print(f"Le deuxième qualifié au second tour est {turn_1[1][0]}")
    print(f"Le gagnant du vote au second tour est {turn_2[0][0]}")
    return results

def alternative_vote(voters):
    results = {}
    majority = False
    nb_cand = len(voters[0])
    eliminated = []
    for i in range(nb_cand-1):
        turn = order_results(get_votes_distribution(voters, eliminated))
        if turn[0][1] > len(voters) / 2 and not majority: 
            print(f"Majorité absolue pour {turn[0][0]}")
            majority = True
        eliminated.append(turn[-1][0])
        results[f'turn_{i}']=turn
        print(f"Le candidat éliminé au tour {i} est {turn[-1][0]}")
    print(f"Le gagnant du vote alternatif est {turn[0][0]}")
    return results

def condorcet(voters):
    nb_cand = len(voters[0])
    votes = [[0 for i in range(nb_cand)] for j in range(nb_cand)]
    wins = [0 for i in range(nb_cand)]
    for i in range(nb_cand):
        for j in range(i+1, nb_cand):
            skipped = {k+1 for k in range(nb_cand)}
            skipped -= {i+1, j+1}
            duel = get_votes_distribution(voters, list(skipped))
            votes[i][j] = duel[i]
            votes[j][i] = duel[j]
            if duel[i] > duel[j]: wins[i] += 1
            else: wins[j] += 1
    return order_results(wins), votes

def borda(voters):
    candidates_number = len(voters[0])
    results = [0 for i in range(candidates_number)]
    score = candidates_number-1
    for i in range(candidates_number-1):
        for j in range(len(voters)):
            results[voters[j][i]-1] += score
        score-=1
    return order_results(results)

def coombs(voters):
    steps ={}
    eliminated = []
    candidates_number = len(voters[0])
    for i in range(candidates_number-1):
        result = get_votes_distribution(voters, eliminated=eliminated)
        steps[f"turn_{i}"] = order_results(result)
        if absolute_majority(result): return steps
        hated = get_votes_distribution(voters, eliminated=eliminated, reverse=True)
        most_hated = np.argmax(hated) + 1
        eliminated.append(most_hated)


LETTER_TO_NUMBER = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "F": 6,
    "G": 7,
    "H": 8,
    "I": 9,
}

from typing import List, Dict, Tuple, Union, FrozenSet

def letters_to_vote(letters: List[tuple]):
    """_summary_
    Args:
        dict_letters (dict): format {[A,B,D]: 3, ...}
    """
    new_list = []
    for i in letters:
        order = [LETTER_TO_NUMBER[x] for x in i[0]]
        for j in range(i[1]):
            new_list.append(order)
    # print(new_list)
    return new_list
            


schulze_test_data = [
    [list("ACBED"), 5],
    [list("ADECB"), 5],
    [list("BEDAC"), 8],
    [list("CABED"), 3],
    [list("CAEBD"), 7],
    [list("CBADE"), 2],
    [list("DCEBA"), 7],
    [list("EBADC"), 8],
]

def schulze(voters):
    # distance matrix between voters
    _, d = condorcet(voters)
    return strongest_path_strengths(d, len(voters[0]))

def strongest_path_strengths(d, c):
    p = [[0 for i in range(c)] for j in range(c)]
    for i in range(c):
        for j in range(c):
            if i != j :
                if d[i][j] > d[j][i]:
                    p[i][j] = d[i][j]
                else:
                    p[i][j] = 0
    for i in range(c):
        print(p[i])
    print("")
    for i in range(c):
        for j in range(c):
            if i != j :
                for k in range(c):
                    if i != k and j != k:
                        p[j][k] = max (p[j][k], min (p[j][i], p[i][k]))
    for i in range(c):
        print(p[i])
    return


