from datawrapper import MetaTransformDataWrapper
import json
import unittest

class TestTransform(unittest.TestCase):
    def setUp(self):
        self.data = MetaTransformDataWrapper(
            {'my_data': 1},
            [{'my_target': 2}]
        )

    def test_instance(self):
        
        expected = {'data': {'my_data': 1}, 'target': [{'my_target': 2}]}

        self.assertDictEqual(expected, self.data.to_dict())

    def test_data(self):

        expected = {'my_data': 1}

        self.assertDictEqual(expected, self.data.data)

    def test_target(self):
        
        expected = [{'my_target': 2}]

        self.assertListEqual(expected, self.data.target)


if __name__ == "__main__":
    unittest.main()