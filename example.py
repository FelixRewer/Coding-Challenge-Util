from CCUtil import run

#
# This is an usage example.
# Here you can see how to use the
# run-decorator.
# To run this, just execute this file
# (nothing else needed than the CCUtil.py)
#


@run(challenge=2, times=10, additional="sorted")
def doit(order: dict):
    return order["list"].index(order["k"])

# The last line of the output should be something like:
# Result: Took 0.00677 ms on average with a 100.000% success rate
