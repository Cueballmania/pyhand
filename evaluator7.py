# Create all of the 7 card hand evaluations
# Procedure:
# 1. Count the number of each suit in the 7-card hand
# 2a. If the number of any suit is fewer than 5, then the hand does a prime-factorization lookup
# 2b. If the number of any suit is 5 or 6, the only possible best hand is a flush or straight flush
# 2b1. If the number of that suit is 5, use the 5 card flush lookup
# 2b2. If the number of that suit is 6, take the greatest of the 5 - 5 card flush lookups
# 2c. If there is only one suit (7 cards in that suit), then the best hand is a flush or straight flush
#     use the computed 7-card flush lookup
:while