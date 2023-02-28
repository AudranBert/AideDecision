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
    return order_results(get_votes_distribution(voters))

def two_turn_vote(voters, candidates_number=2):
    results = dict()
    turn_1 = one_turn_vote(voters)
    results[f'turn_1'] = turn_1
    eliminated = [x[0]-1 for i, x in enumerate(turn_1) if i>=candidates_number-1]
    results[f'turn_2'] =  order_results(get_votes_distribution(voters, eliminated))
    return results


def alternative_vote(voters):
    results = {}
    number_of_candidates = len(voters[0])
    eliminated = []
    for i in range(number_of_candidates):
        turn = order_results(get_votes_distribution(voters, eliminated))
        eliminated.append(turn[-1][0])
        results[f'turn_{i}']=turn
        # print(eliminated)
    return results

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
    eliminated = []
    candidates_number = len(voters[0])
    for i in range(candidates_number-1):
        result = get_votes_distribution(voters, eliminated=eliminated)
        if absolute_majority(result): return result
        hated = get_votes_distribution(voters, eliminated=eliminated, reverse=True)
        most_hated = np.argmax(hated) + 1
        eliminated.append(most_hated) 
    return result