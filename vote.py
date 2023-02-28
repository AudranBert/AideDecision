import numpy as np

def get_votes_distribution(voters, elimineted=[], reverse=False):
    candidates_number = len(voters[0])
    rank = 0 if not reverse else candidates_number-1
    distribution = [0 for i in range(candidates_number)]
    for pref in voters:
        current_choice = rank
        while pref[current_choice] in elimineted:
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



def one_turn_vote(voters):
    return order_results(get_votes_distribution(voters))

def two_turn_vote(voters, candidates_number=2):
    turn_1 = one_turn_vote(voters)
    eliminated = [x[0]-1 for i, x in enumerate(turn_1) if i>=candidates_number-1]
    return order_results(get_votes_distribution(voters, eliminated))


# def alternative_vote(voters):
#     result = []
#     for vote in voters:
#         turn = get_votes_distribution(voters, r)
