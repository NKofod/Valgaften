'''
Assignment for Algorithms and Data Structures - Seat Allocation.
Calculates the result of a fictional election. 
Input: 
On the first line of input: the number 'n' of parties and 'm' of seats.
On each of the following 'n' lines, the integer v_i representing the number
of votes for each party. 
Output: 
'n' lines containing the number of seats obtained by each party
'''

# Import dependencies 
from fileinput import FileInput

# Read in the data 
data = FileInput()
data = [i.strip() for i in data]

# Instantiate the number of parties and number of seats
parties, seats = data[0].split(" ")

# Update the data 
data = data[1:]

# Instantiate five lists - votes (representing the current number of 
# votes each party has after dividing with a quotient), votes_raw (the total
# number of votes a party uptained before a quotient is applied), quotient (
# representing the current quotient) and party_seats (representing the current 
# number of seats uptained)
votes = [int(data[i]) for i in range(int(parties))]
votes_raw = [int(data[i]) for i in range(int(parties))]
party = [i for i in range(int(parties))]
quotient = [1] * int(parties)
party_seats = [0] * int(parties)

# For each seat, find the maximum value of the votes-list and update the votes,
# quotient and party_seats lists.  
for i in range(int(seats)):
    winner = votes.index(max(votes))
    quotient[winner] += 1
    party_seats[winner] += 1
    votes[winner] = votes_raw[winner] / quotient[winner]

# Loop over the party_seats list and print the result. 
for i in party_seats:
    print(i)

