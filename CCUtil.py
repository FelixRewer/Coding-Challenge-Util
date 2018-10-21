import time
import requests
import json
import statistics
import warnings

BASE_URL = "https://cc.the-morpheus.de/"


def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)

        return repl

    return layer


@parametrized
def cc(method, **kwargs):
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

    assert "challenge" in kwargs, "The argument 'challenge' must be defined."

    if "times" not in kwargs:
        multiple = 10
    else:
        multiple = kwargs["times"]
        assert multiple >= 1, "The argument 'times' must be more than 0."

    challenge_id = str(kwargs["challenge"])
    path = challenge_id + "/" + str(kwargs["additional"]) if "additional" in kwargs else challenge_id
    challenge_url = f"{BASE_URL}challenges/{path}/"
    solution_url = f"{BASE_URL}solutions/{challenge_id}/"

    assert requests.get(challenge_url).status_code != 404, "Challenge doesn't exist."

    exceptions = [{"id": 9, "message": "Sometimes your solution might cause an error though it's right."}]

    for exception in exceptions:
        if int(challenge_id) == exception["id"]:
            warnings.warn(exception["message"], Warning)

    success = 0
    times = []

    

    for k in range(multiple):
        task = requests.get(challenge_url)
        try:
            task = task.json()
        except:
            task = task.text
        ts = time.time()
        function_response = method(task)
        times.append((time.time() - ts) * 1000)
        solution_response = requests.post(solution_url, json.dumps({"token": function_response}))
        if solution_response.status_code == 500 or "Error" in solution_response.text:
            try:
                taskstr = json.dumps(task)
            except:
                taskstr = str(task)
            print(f"# {k + 1} Wrong: {taskstr} {function_response}")
        else:
            success += 1
            print(f"# {k + 1} {solution_response.text}")

    times = statistics.mean(times)
    success_rate = success / multiple * 100
    print(f"> Result for challenge {challenge_id}: Took {times:2.5f} ms on average with a {success_rate:3.3f} % success rate")
