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

    def test_insert_queue_handling(self):
        q = t.MorreQueue()
        self.assertEqual(0, q.insert_queue_length)
        q._add_to_insert_queue()
        self.assertEqual(0, q.insert_queue_length)
        q._add_to_insert_queue([])
        self.assertEqual(0, q.insert_queue_length)

        q = t.MorreQueue()
        q._add_to_insert_queue([self.c1])
        self.assertEqual(1, q.insert_queue_length)
        q._add_to_insert_queue([self.c2, self.c3])
        self.assertEqual(3, q.insert_queue_length)
        i: SeekContentBlob = q._pop_from_insert_queue()
        self.assertEqual(2, q.insert_queue_length)
        self.assertEqual(0, q.delete_queue_length)
        self.assertEqual(self.c3, i)
        i: SeekContentBlob = q._pop_from_insert_queue()
        self.assertEqual(1, q.insert_queue_length)
        self.assertEqual(self.c2, i)
        i: SeekContentBlob = q._pop_from_insert_queue()
        self.assertEqual(0, q.insert_queue_length)
        self.assertEqual(self.c1, i)

    def test_insert_queue_exceptions(self):
        with pytest.raises(TypeError) as e:
            f = t.MorreQueue()
            f._add_to_insert_queue([42])

        q = t.MorreQueue()
        q._add_to_insert_queue([self.c1])
        with pytest.raises(TypeError) as e:
            q._add_to_insert_queue([42])

    def test_insert_queue_consistency(self):
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

    def test_delete_queue_handling(self):
        q = t.MorreQueue()
        self.assertEqual(0, q.delete_queue_length)
        q._add_to_delete_queue()
        self.assertEqual(0, q.delete_queue_length)
        q._add_to_delete_queue([])
        self.assertEqual(0, q.delete_queue_length)

        q = t.MorreQueue()
        q._add_to_delete_queue([self.c1.link_to_model])
        self.assertEqual(1, q.delete_queue_length)
        q._add_to_delete_queue([self.c2.link_to_model, self.c3.link_to_model])
        self.assertEqual(3, q.delete_queue_length)
        i: str = q._pop_from_delete_queue()
        self.assertEqual(2, q.delete_queue_length)
        self.assertEqual(0, q.insert_queue_length)
        self.assertTrue(i.startswith("bla"))
        i: str = q._pop_from_delete_queue()
        self.assertEqual(1, q.delete_queue_length)
        self.assertTrue(i.startswith("bla"))
        i: str = q._pop_from_delete_queue()
        self.assertEqual(0, q.delete_queue_length)
        self.assertTrue(i.startswith("bla"))

    def test_update_queue_handling(self):
        q = t.MorreQueue()
        self.assertEqual(0, q.delete_queue_length)
        self.assertEqual(0, q.insert_queue_length)
        q._add_to_update_queue()
        self.assertEqual(0, q.delete_queue_length)
        self.assertEqual(0, q.insert_queue_length)
        q._add_to_update_queue([])
        self.assertEqual(0, q.delete_queue_length)
        self.assertEqual(0, q.insert_queue_length)

        q = t.MorreQueue()
        q._add_to_update_queue([self.c1])
        self.assertEqual(1, q.delete_queue_length)
        self.assertEqual(1, q.insert_queue_length)
        q._add_to_update_queue([self.c2, self.c3])
        self.assertEqual(3, q.delete_queue_length)
        self.assertEqual(3, q.insert_queue_length)
        i: str = q._pop_from_delete_queue(self.c2)
        self.assertEqual(2, q.delete_queue_length)
        self.assertEqual(3, q.insert_queue_length)
        self.assertEqual(self.c2.link_to_model, i)
        i: str = q._pop_from_delete_queue()
        self.assertEqual(1, q.delete_queue_length)
        self.assertEqual(3, q.insert_queue_length)
        self.assertEqual(self.c3.link_to_model, i)
        i: str = q._pop_from_delete_queue()
        self.assertEqual(0, q.delete_queue_length)
        self.assertEqual(3, q.insert_queue_length)
        self.assertEqual(self.c1.link_to_model, i)
