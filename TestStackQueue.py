import unittest
from stackqueue import Stack, Queue



class TestStack(unittest.TestCase):
    def test_push_and_pop_order(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.push(3)
        self.assertEqual(s.pop(), 3)  # last pushed comes out first
        self.assertEqual(s.pop(), 2)
        self.assertEqual(s.pop(), 1)

    def test_peek_does_not_remove(self):
        s = Stack()
        s.push(1)
        s.push(2)
        self.assertEqual(s.peek(), 2)
        self.assertEqual(len(s), 2)  # peek didn't remove anything

    def test_is_empty(self):
        s = Stack()
        self.assertTrue(s.is_empty())
        s.push(1)
        self.assertFalse(s.is_empty())

    def test_pop_empty_raises(self):
        s = Stack()
        with self.assertRaises(IndexError):
            s.pop()

    def test_peek_empty_raises(self):
        s = Stack()
        with self.assertRaises(IndexError):
            s.peek()

    def test_len(self):
        s = Stack()
        s.push(1)
        s.push(2)
        self.assertEqual(len(s), 2)


class TestQueue(unittest.TestCase):
    def test_enqueue_and_dequeue_order(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        self.assertEqual(q.dequeue(), 1)  # first enqueued comes out first
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), 3)

    def test_peek_does_not_remove(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        self.assertEqual(q.peek(), 1)
        self.assertEqual(len(q), 2)

    def test_is_empty(self):
        q = Queue()
        self.assertTrue(q.is_empty())
        q.enqueue(1)
        self.assertFalse(q.is_empty())

    def test_dequeue_empty_raises(self):
        q = Queue()
        with self.assertRaises(IndexError):
            q.dequeue()

    def test_peek_empty_raises(self):
        q = Queue()
        with self.assertRaises(IndexError):
            q.peek()

    def test_len(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        self.assertEqual(len(q), 2)


if __name__ == "__main__":
    unittest.main()