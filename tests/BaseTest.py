import unittest

class BaseTest(unittest.TestCase):
     def setUp(self):
        self.data = 'HelloWorld!'

     def test(self):
         result = 'HelloWorld!'

         self.assertEqual(self.data, result)
