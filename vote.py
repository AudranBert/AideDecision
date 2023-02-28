import numpy as np

def get_votes_distribution(voters, rank=0):
    distribution = [0 for i in range(len(voters[0]))]
    for pref in voters:
        distribution[pref[0] - 1] += 1
    return distribution



def order_results(vote_distribution_results):
    results = []
    for i, votes in enumerate(vote_distribution_results):
        results.append((i+1, votes))
    return sorted(
        results, 
        key=lambda x: x[1],
        reverse=True
    )



def one_turn_vote(voters):
    return order_results(get_votes_distribution(voters))

def two_turn_vote(voters):
    turn_1 = one_turn_vote(voters)
    eliminated = [x[0]-1 for i, x in enumerate(turn_1) if i>=2]
    print(eliminated)


# def alternative_vote(voters):
#     result = []
#     for vote in voters:
#         turn = get_votes_distribution(voters, r)