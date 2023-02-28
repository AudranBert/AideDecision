def get_votes_distribution(voters, rank=0):
    distribution = [0 for i in range(len(voters[0]))]
    for pref in voters:
        distribution[pref[0] - 1] += 1
    return distribution
