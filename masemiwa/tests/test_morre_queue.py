from unittest import TestCase

import pytest

import masemiwa.morre_queue as t


class TestMorreQueue(TestCase):
    def test_queue_handling(self):
        q = t.MorreQueue()
        self.assertEqual(0, q.queue_length)
        q = t.MorreQueue([])
        self.assertEqual(0, q.queue_length)
        q._add_to_queue()
        self.assertEqual(0, q.queue_length)
        q._add_to_queue([])
        self.assertEqual(0, q.queue_length)

        q = t.MorreQueue(["ui"])
        self.assertEqual(1, q.queue_length)
        q._add_to_queue(["bla", "blubb"])
        self.assertEqual(3, q.queue_length)
        i: str = q._pop()
        self.assertEqual(2, q.queue_length)
        self.assertEqual("blubb", i)
        i: str = q._pop()
        self.assertEqual(1, q.queue_length)
        self.assertEqual("bla", i)
        i: str = q._pop()
        self.assertEqual(0, q.queue_length)
        self.assertEqual("ui", i)

    def test_queue_exceptions(self):
        with pytest.raises(TypeError) as e:
            t.MorreQueue([42])

        q = t.MorreQueue(["ui"])
        with pytest.raises(TypeError) as e:
            q._add_to_queue([42])

    def test_queue_consistency(self):
        q1: list = ['bla', 'blo', 'blu', 'bli', 'ui']
        q1_tmp: list = q1.copy()
        self.assertEqual(q1, q1_tmp)
        q1.append('hui')
        self.assertNotEqual(q1, q1_tmp)
        q1 = q1_tmp.copy()

        m = t.MorreQueue(q1)
        self.assertEqual(q1, q1_tmp)
        m._add_to_queue(['qwert', 'zuiopü'])
        self.assertEqual(q1, q1_tmp)
