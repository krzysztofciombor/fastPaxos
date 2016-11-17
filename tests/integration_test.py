import unittest
import os
from client import main, reset, get_value
import time


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        os.system("python3 fast_paxos.py 5000 6 > /dev/null 2> /dev/null &")

        for x in range(1, 7):
            cmd = "python3 Instance.py 500" + str(x)
            os.system(cmd + " 6 > /dev/null 2> /dev/null &")

        time.sleep(5)

    def tearDown(self):
        os.system("pkill -f fast_paxos.py")
        os.system("pkill -f Instance.py")

    def test_optimistic_case(self):
        reset(1)
        main(127)
        time.sleep(5)
        value = get_value()
        assert int(value) == 127

    def test_inactive_nodes_case(self):
        reset(2)
        main(127)
        time.sleep(5)
        value = get_value()
        assert int(value) == 127

    def test_failing_nodes_case(self):
        reset(3)
        main(127)
        time.sleep(5)
        value = get_value()
        assert int(value) == 127

    def test_simultaneous_requests_case(self):
        reset(4)
        main(127)
        main(721)
        time.sleep(5)
        value = get_value()
        assert int(value) == 127
