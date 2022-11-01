


def district_vote_quotient(parties,votes,seats): 
    votes_raw = votes
    quotient = [1] * len(parties)
    party_seats = [0] * len(parties)
 
    for i in range(int(seats)):
        winner = votes.index(max(votes))
        quotient[winner] += 1
        party_seats[winner] += 1
        votes[winner] = votes_raw[winner] / quotient[winner]
    results = {}
    for idx,party in enumerate(parties):
        results[party] = party_seats[idx]
    return results 

