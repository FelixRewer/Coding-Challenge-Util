import time
import requests
import json
import statistics

BASE_URL = "https://cc.the-morpheus.de/"


def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)

        return repl

    return layer


@parametrized
def run(method, **kwargs):
    """
    Possible **kwargs for the decorator:

    times:
        The number of times the implementations should be tested.
    challenge:
        The challenge-id as an integer.
    additional:
        A string that will be added after the challenge url,
        for example, if additional is "sorted" and challenge is 2,
        then "challenge_url" is https://cc.the-morpheus.de/challenges/2/sorted/
        instead of https://cc.the-morpheus.de/challenges/2/

    :param method:
    :param kwargs:
    :return:
    """

    if "challenge" not in kwargs:
        print("Nope.")
        exit(1)

    if "times" not in kwargs:
        multiple = 1
    else:
        multiple = kwargs["times"]
        assert multiple >= 1, "No..."

    challenge_id = str(kwargs["challenge"])
    argz = challenge_id + "/" + str(kwargs["additional"]) if "additional" in kwargs else challenge_id
    challenge_url = f"{BASE_URL}challenges/{argz}/"
    solution_url = f"{BASE_URL}solutions/{challenge_id}/"

    success = 0
    times = []

    for k in range(multiple):
        order = requests.get(challenge_url)
        try:
            order = order.json()
        except:
            order = order.text
        ts = time.time()
        function_response = method(order)
        times.append((time.time() - ts) * 1000)
        solution_response = requests.post(solution_url, json.dumps({"token": function_response}))
        if solution_response.status_code == 500 or "Error" in solution_response.text:
            print("#", k + 1, "Wrong:", order, function_response)
        else:
            success += 1
            print("#", k + 1, solution_response.text)

    times = statistics.mean(times)
    success_rate = success / multiple * 100
    print(f"\n# Result: Took {times:2.5f} ms on average with a {success_rate:3.3f} % success rate")
