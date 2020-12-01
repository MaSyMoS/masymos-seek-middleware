from unittest import TestCase

import pytest

import masemiwa.morre_queue as t
from masemiwa.input_analyser.beans import SeekContentBlob


class TestMorreQueue(TestCase):
    c1: SeekContentBlob = SeekContentBlob({'content_type': 'blo1', 'link': 'bla1'})
    c2: SeekContentBlob = SeekContentBlob({'content_type': 'blo2', 'link': 'bla2'})
    c3: SeekContentBlob = SeekContentBlob({'content_type': 'blo3', 'link': 'bla3'})
    c4: SeekContentBlob = SeekContentBlob({'content_type': 'blo4', 'link': 'bla4'})
    c5: SeekContentBlob = SeekContentBlob({'content_type': 'blo5', 'link': 'bla5'})

    def test_queue_handling(self):
        q = t.MorreQueue()
        self.assertEqual(0, q.queue_length)
        q._add_to_insert_queue()
        self.assertEqual(0, q.queue_length)
        q._add_to_insert_queue([])
        self.assertEqual(0, q.queue_length)

        q = t.MorreQueue()
        q._add_to_insert_queue([self.c1])
        self.assertEqual(1, q.queue_length)
        q._add_to_insert_queue([self.c2, self.c3])
        self.assertEqual(3, q.queue_length)
        i: SeekContentBlob = q._pop()
        self.assertEqual(2, q.queue_length)
        self.assertEqual(self.c3, i)
        i: SeekContentBlob = q._pop()
        self.assertEqual(1, q.queue_length)
        self.assertEqual(self.c2, i)
        i: SeekContentBlob = q._pop()
        self.assertEqual(0, q.queue_length)
        self.assertEqual(self.c1, i)

    def test_queue_exceptions(self):
        with pytest.raises(TypeError) as e:
            f = t.MorreQueue()
            f._add_to_insert_queue([42])

        q = t.MorreQueue()
        q._add_to_insert_queue([self.c1])
        with pytest.raises(TypeError) as e:
            q._add_to_insert_queue([42])

    def test_queue_consistency(self):
        q1: list = [self.c1, self.c2, self.c3]
        q1_tmp: list = q1.copy()
        self.assertEqual(q1, q1_tmp)
        q1.append(self.c4)
        self.assertNotEqual(q1, q1_tmp)

        q1 = q1_tmp.copy()
        m = t.MorreQueue()
        m._add_to_insert_queue(q1)
        self.assertEqual(q1, q1_tmp)
        m._add_to_insert_queue([self.c5])
        self.assertEqual(q1, q1_tmp)

# TODO add more tests, delete, update
