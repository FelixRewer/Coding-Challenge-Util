# Coding Challenge Util
This Coding Challenge Util is made to make
the code more readable for the different implementations
of different solutions of different "solvers".


## How to use
How to use this function is shown in example.py, but here is a short recap:
```python
from CodingChallengeUtil import run

@run(challenge=2, times=10, additional="sorted")
def doit(order: dict):
    return order["list"].index(order["k"])
```
* times

   The number of times the implementations should be tested.
* challenge
    
    The challenge-id as an integer.
* additional 

   A string that will be added after the challenge url,
   for example, if additional is "sorted" and challenge is 2,
   then "challenge_url" is https://cc.the-morpheus.de/challenges/2/sorted/
   instead of https://cc.the-morpheus.de/challenges/2/

## Expected output
```
...
# 8 Success: TMT{...}
# 9 Success: TMT{...}
# 10 Success: TMT{...}

# Result: Took 0.00803 ms on average with a 100.000 % success rate
```
