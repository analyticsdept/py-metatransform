from metatransform import MetaTransform
import json
import unittest

class TestTransform(unittest.TestCase):
    def setUp(self):
        self.transform = MetaTransform()

    def test_cast_list_delimited(self):
        input = "1,2,3,4"
        expected = ["1", "2", "3", "4"]
        self.assertEqual(self.transform.cast_list(input, ","), expected, f"Should be {expected}")

    def test_cast_list(self):
        input = "1,2,3,4"
        expected = ["1,2,3,4"]
        self.assertEqual(self.transform.cast_list(input), expected, f"Should be {expected}")

    def test_cast_dict_string(self):
        input = "my string"
        expected = {"0": "my string"}
        self.assertEqual(self.transform.cast_dict(input), expected, f"Should be {expected}")

    def test_cast_dict_int(self):
        input = 1
        expected = {"0": 1}
        self.assertEqual(self.transform.cast_dict(input), expected, f"Should be {expected}")

    def test_cast_dict_float(self):
        input = 1.0049494
        expected = {"0": 1.0049494}
        self.assertEqual(self.transform.cast_dict(input), expected, f"Should be {expected}")

    def test_cast_dict_bool(self):
        input = True
        expected = {"0": True}
        self.assertEqual(self.transform.cast_dict(input), expected, f"Should be {expected}")

    def test_cast_dict_list(self):
        input = [1, 2, 3, 4]
        expected = {0: 1, 1: 2, 2: 3, 3: 4}
        self.assertEqual(self.transform.cast_dict(input), expected, f"Should be {expected}")

    def test_cast_dict_list_delimited(self):
        input = "1,2,3,4"
        expected = {0: "1", 1: "2", 2: "3", 3: "4"}
        self.assertEqual(self.transform.cast_dict(input, list_delimiter=","), expected, f"Should be {expected}")
    
    def test_cast_dict_list_key_delimited(self):
        input = "a:1,b:2,c:3,d:4"
        expected = {"a": "1", "b": "2", "c": "3", "d": "4"}
        self.assertEqual(self.transform.cast_dict(input, list_delimiter=",", key_delimiter=":"), expected, f"Should be {expected}")

    def test_cast_bool_string(self):
        input = "my string"
        expected = True
        self.assertEqual(self.transform.cast_bool(input), expected, f"Should be {expected}")

    def test_cast_string_string(self):
        input = "my string"
        expected = "my string"
        self.assertEqual(self.transform.cast_string(input), expected, f"Should be {expected}")
    
    def test_cast_string_int(self):
        input = 123
        expected = "123"
        self.assertEqual(self.transform.cast_string(input), expected, f"Should be {expected}")

    def test_cast_string_float(self):
        input = 0.1234
        expected = "0.1234"
        self.assertEqual(self.transform.cast_string(input), expected, f"Should be {expected}")

    def test_cast_string_list(self):
        input = [1,2,3,4]
        expected = "1,2,3,4"
        self.assertEqual(self.transform.cast_string(input), expected, f"Should be {expected}")

    def test_cast_string_dict(self):
        input = {"key_1": 1, "key_2": "2"}
        expected = "key_1:1,key_2:2"
        self.assertEqual(self.transform.cast_string(input), expected, f"Should be {expected}")

    def test_cast_string_bool(self):
        input = True
        expected = "true"
        self.assertEqual(self.transform.cast_string(input), expected, f"Should be {expected}")

    def test_lowercase(self):
        input = "MY STRING"
        expected = "my string"
        self.assertEqual(self.transform.lowercase(input), expected, f"Should be {expected}")

    def test_uppercase(self):
        input = "my string"
        expected = "MY STRING"
        self.assertEqual(self.transform.uppercase(input), expected, f"Should be {expected}")

    def test_remap_fields(self):
        input = {
            "field1": "f1value",
            "object1": {
                "objectchild1": 1234
            },
            "object2": {
                "objectchild2": 1234
            },
            "object3": [{
                "objectchild3.1": 1234
            }, {
                "objectchild3.2": [5,6,7,8]
            }, {
                "objectchild3.2": [9,10,11,12]
            }],
            "kola": [{
                "param1": 1,
                "param2": [{
                    "nested_param1": 2,
                    "nested_param2": [3,4,5,6]
                }]
            }],
            "array1": [5,6,7,8],
            "array2": [10, 11, 12, 13]
        }
        map = {
            "field1": {"_name": "field_1"},
                "object1": {
                    "_name": "object_1",
                    "objectchild1": {"_name": "object_child_1", "_type": "list"}
                },
                "object2": {
                    "_name": "object_2",
                    "_type": "list",
                    "objectchild2": {"_name": "object_child_2", "_type": "string"}
                },
                "object3": {
                    "_name": "list_of_objects",
                    "_list": {
                        "objectchild3.2": {
                            "_name": "objectchild3.2.0.1",
                            "_type": "string"
                        }
                    }
                },
                "kola": {
                    "_name": "super-deep",
                    "_list": {
                        "param1": {"_name": "first_parameter", "_type": "string"},
                        "param2": {
                            "_name": "second_parameter",
                            "_list": {
                                "nested_param2": {"_type": "string"}
                            }
                        }
                    }
                },
                "array1": {"_name": "array_1"},
                "array2": {"_type": "string"}
        }
        expected = {
            "field_1": "f1value",
                "object_1": {
                    "object_child_1": [1234]
                },
                "object_2": [{
                    "object_child_2": "1234"
                }],
                "list_of_objects": [{
                    "objectchild3.1": 1234
                }, {
                    "objectchild3.2.0.1": "5,6,7,8"
                }, {
                    "objectchild3.2.0.1": "9,10,11,12"
                }],
                "super-deep": [{
                    "first_parameter": "1",
                    "second_parameter": [{
                        "nested_param1": 2,
                        "nested_param2": "3,4,5,6"
                    }]
                }],
                "array_1": [5,6,7,8],
                "array2": "10,11,12,13"
        }
        _target_input = json.loads(json.dumps(input))
        
        result = self.transform.remap_fields(_target_input, map)
        
        self.assertDictEqual(result, expected)

    def test_remap_fields_on_list(self):
        input = [{
            "field_1": 1,
            "field_2": {
                "field_2_a": 2
            },
            "field_3": [{
                "field_3_a": 10
            }]
        }, {
            "field_1": 3,
            "field_2": {
                "field_2_a": 4
            },
            "field_3": [{
                "field_3_a": 10
            }]
        }]
        map = {
            "field_1": {
                "_name": "field_100"
            },
            "field_2": {
                "field_2_a": {
                    "_type": "string"
                }
            }
        }
        expected = [{
            "field_100": 1,
            "field_2": {
                "field_2_a": "2"
            },
            "field_3": [{
                "field_3_a": 10
            }]
        }, {
            "field_100": 3,
            "field_2": {
                "field_2_a": "4"
            },
            "field_3": [{
                "field_3_a": 10
            }]
        }]
        
        _target_input = json.loads(json.dumps(input))
        
        result = self.transform.remap_fields(_target_input, map)

        self.assertListEqual(result, expected)

    def test_flatten_dict(self):
        input = {
            "field_1": "a string",
            "field_2": {
                "field_2.1": 1234,
                "field_2.2": "another string"
            },
            "field_3": [
                "list_string_1",
                "list_string_2",
            ],
            "field_4": [
                {"field_4_item_1_key_1": "hello", "field_4_item_1_key_2": 5678},
                {"field_4_item_2_key_1": "bye"}
            ],
            "field_5": [],
            "field_6": {},
            "field_7": "",
            "field_8": None
        }
        expected = {
            "field_1": "a string",
            "field_2_-_field_2.1": 1234,
            "field_2_-_field_2.2": "another string",
            "field_3_-_0": "list_string_1",
            "field_3_-_1": "list_string_2",
            "field_4_-_0_-_field_4_item_1_key_1": "hello", 
            "field_4_-_0_-_field_4_item_1_key_2": 5678,
            "field_4_-_1_-_field_4_item_2_key_1": "bye",
            "field_5": [],
            "field_6": {},
            "field_7": "",
            "field_8": None
        }
        flattened = self.transform.flatten_dict(input)
        self.assertDictEqual(flattened, expected)

    def test_flatten_dict_on_list(self):
        input = [{
            "field_1": "a string",
            "field_2": {
                "field_2.1": 1234,
                "field_2.2": "another string"
            },
            "field_3": [
                "list_string_1",
                "list_string_2",
            ]
        }, {
            "field_1": "another string",
            "field_2": {
                "field_2.1": 5678,
                "field_2.2": "yet another string"
            },
            "field_3": [
                "list_string_1_A",
                "list_string_2_B",
            ]
        }]
        expected = [{
            "field_1": "a string",
            "field_2__field_2.1": 1234,
            "field_2__field_2.2": "another string",
            "field_3__0": "list_string_1",
            "field_3__1": "list_string_2",
        }, {
            "field_1": "another string",
            "field_2__field_2.1": 5678,
            "field_2__field_2.2": "yet another string",
            "field_3__0": "list_string_1_A",
            "field_3__1":"list_string_2_B"
        }]
        chain = [{
            "flatten": {
                "delimiter": "__",
                "exclude": []
            }
        }]

        result = self.transform.transform(input, chain)

        self.assertListEqual(result['data'], expected)

    def test_subroutine(self):
        input = {
            "field_1": [1,2,3,4]
        }
        expected = {
            "field_1": "1,2,3,4"
        }
        chain = [
            {"sub1": True},
            {"sub2": True}
        ]
        
        subroutines = [{
            "sub1": [{
                "remap_fields": {
                    "field_1": {
                        "_type": "string"
                    }
                }
            }]
            }, {
            "sub2": [{
                "flatten": {
                    "delimiter": "__",
                    "exclude": []
                }
            }]
        }]

        result = self.transform.transform(input, chain, subroutines)
        
        self.assertDictEqual(result['data'][0], expected)

    def test_filter_field_value(self):
        input = {
            "event_name": "view_screen"
        }
        expected = True
        field = {
            "event_name": "view_screen"
        }
        result = self.transform.filter_field_value(input, field)
        self.assertEqual(result, expected)

    def test_filter_field_value_deep(self):
        input = {
            "session": {
                "id": "1234"
            }
        }
        expected = True
        field = {
            "session": {
                "id": "1234"
            }
        }
        result = self.transform.filter_field_value(input, field)
        self.assertEqual(result, expected)

    def test_filter_field_value_deep_list(self):
        input = {
            "session": [{
                "id": "1234"
            }]
        }
        expected = True
        field = {
            "session": [{
                "id": "1234"
            }]
        }
        result = self.transform.filter_field_value(input, field)
        self.assertEqual(result, expected)

    def test_filter_field_value_deep_list_no_list(self):
        input = {
            "session": [{
                "id": "1234"
            }]
        }
        expected = True
        field = {
            "session": {
                "id": "1234"
            }
        }
        result = self.transform.filter_field_value(input, field)
        self.assertEqual(result, expected)

    def test_filter_field_value_deep_list_one_match_first(self):
        input = {
            "session": [{
                "id": "1234"
            }, {
                "id": "5678"
            }]
        }
        expected = True
        field = {
            "session": [{
                "id": "1234"
            }]
        }
        result = self.transform.filter_field_value(input, field)
        self.assertEqual(result, expected)

    def test_filter_field_value_deep_list_one_match_second(self):
        input = {
            "session": [{
                "id": "1234"
            }, {
                "id": "5678"
            }]
        }
        expected = True
        field = {
            "session": [{
                "id": "5678"
            }]
        }
        result = self.transform.filter_field_value(input, field)
        self.assertEqual(result, expected)

    def test_filter_field_value_on_list(self):
        input = [{
            "session": [{
                "id": "1234"
            }, {
                "id": "5678"
            }]
        }, {
            "session": [{
                "id": "91011"
            }, {
                "id": "121314"
            }]
        }]
        expected = [{
            "session": [{
                "id": "91011"
            }, {
                "id": "121314"
            }]
        }]
        field = {
            "session": [{
                "id": "91011"
            }]
        }
        chain = [{
            "filter_field_value": field
        }]
        
        result = self.transform.transform(input, chain)

        self.assertEqual(result['data'], expected)

    def test_filter_field_value_multiple_conditions(self):
        input = {
            "event_params": [{
                "key": "api_status",
                "value": {
                    "integer": 200
                }
            }]
        }
        field = [{
            "event_params": {
                "key": "api_status"
            }
        }]
        expected = {
            "event_params": [{
                "key": "api_status",
                "value": {
                    "integer": 200
                }
            }]
        }
        chain = [{
            "filter_field_value": field
        }]

        result = self.transform.transform(input, chain)

        self.assertDictEqual(result['data'], expected)

    def test_filter_field_value_multiple_conditions(self):
        input = [{
            "event_params": [{
                "key": "api_status",
                "value": {
                    "integer": 200
                }
            }]
        }, {
            "event_params": [{
                "key": "api_status",
                "value": {
                    "integer": 203
                }
            }]
        }]
        field = {
            "event_params": {
                "_filter": {
                    "key": "api_status",
                    "value": {
                        "integer": 200
                    }
                }
            }
        }
        expected = [{
            "event_params": [{
                "key": "api_status",
                "value": {
                    "integer": 200
                }
            }]
        }]
        chain = [{
            "filter_field_value": field
        }]
        result = self.transform.transform(input, chain)
        self.assertListEqual(result['data'], expected)


    def test_chain(self):
        input = {
            "field_1": [1,2,3,4],
            "field_2": "5",
            "session": {
                "id": "1_X"
            }
        }
        expected = [{
            "field_1": "1,2,3,4",
            "field_2a": 5,
            "session__id": "1_X",
            "not-a-field": "test-default-value"
        }]
        chain = [
            {"remap_fields": {
                "field_1": {
                    "_type": "string"
                },
                "field_2": {
                    "_name": "field_2a",
                    "_type": "int"
                },
                "session__id": "1_X",
                "not-a-field": {
                    "_default": "test-default-value"
                }
            }},
            {
                "sub2": True
            }
        ]
        subroutines = [{
            "sub2": [{
                "flatten": {
                    "delimiter": "__",
                    "exclude": []
                }
            }]
        }]

        result = self.transform.transform(input, chain, subroutines)

        self.assertListEqual(result['data'], expected)

    def test_filter_subset(self):
        input = {
            "k1": 1,
            "k2": [2,3],
            "k3": {
                "k4": "a"
            }
        }
        subset = ["k1", "k3"]
        expected = {
            "k1": 1,
            "k3": {
                "k4": "a"
            }
        }
        
        result = self.transform.filter_subset(input, subset)

        self.assertDictEqual(result, expected)
    
    def test_filter_subset_on_list(self):
        input = [{
            "k1": 1,
            "k2": [2,3],
            "k3": {
                "k4": "a"
            }
        }, {
            "k1": 5,
            "k2": [6,7],
            "k3": {
                "k4": "b"
            }
        }]
        subset = ["k1", "k3"]
        expected = [{
            "k1": 1,
            "k3": {
                "k4": "a"
            }
        }, {
            "k1": 5,
            "k3": {
                "k4": "b"
            }
        }]

        result = self.transform.filter_subset(input, subset)
        
        self.assertListEqual(result, expected)

    def test_chain_repetition(self):
        input = {
            "f1": 1234,
            "f2": [5,6,7,8],
            "f3": {
                "f4": "x"
            }
        }
        expected = {
            "f_1_1": 1234,
            "f2__0": 5,
            "f2__1": 6,
            "f2__2": 7,
            "f2__3": 8,
            "f3_-____4": "x"
        }
        chain = [
            {"remap_fields": {
                "f1": {"_name": "f_1_1"}
            }},
            {"flatten": {"delimiter":"__"}},
            {"remap_fields": {
                "f3__f4": {"_name": "f3_-____4", "_type": "string"}
            }}
        ]

        result = self.transform.transform(input, chain)

        self.assertDictEqual(result['data'][0], expected)

    def test_process_by_field_value(self):
        input = {
            "event_name": "view_screen",
            "f1": {
                "f2": 1234
            }
        }
        expected = {
            "event_name": "view_screen",
            "f1__f2": 1234
        }
        chain = [{
            "process_by_field_value": {
                "field": "event_name",
                "values": [{
                    "value": "view_screen",
                    "subroutine": "sr_view_screen"
                }]
            }
        }]
        subroutines = [{
            "sr_view_screen": [{
                "flatten": {"delimiter": "__"}
            }]
        }]

        result = self.transform.transform(input, chain, subroutines)

        self.assertDictEqual(result['data'][0], expected)

    def test_process_by_field_value_multiple_values(self):
        input = {
            "event_name": "api_call",
            "f1": {
                "f2": 1234
            }
        }
        expected = {
            "event_name": "api_call",
            "f1_---_f2": 1234
        }
        chain = [{
            "process_by_field_value": {
                "field": "event_name",
                "values": [{
                    "value": "view_screen",
                    "subroutine": "sr_view_screen"
                    }, {
                    "value": "api_call",
                    "subroutine": "sr_api_call"
                }]
            }
        }]
        subroutines = [{
            "sr_view_screen": [{
                "flatten": {"delimiter": "__"}
            }]
        }, {
            "sr_api_call": [{
                "flatten": {"delimiter": "_---_"}
            }]
        }]

        result = self.transform.transform(input, chain, subroutines)

        self.assertDictEqual(result['data'][0], expected)

    def test_process_by_field_value_nested(self):
        input = {
            "event_name": "api_call",
            "f1": {
                "f2": 1234
            }
        }
        expected = {
            "event_name": "api_call",
            "f1_---_f2": 1234
        }
        chain = [{
            "remap_fields": {
                "f1": {
                    "f2": {
                        "_type": "string"
                    }
                }
            }
        },{
            "process_by_field_value": {
                "field": {
                    "f1": "f2"
                },
                "values": [
                    {
                    "value": 5678,
                    "subroutine": "sr_view_screen"
                    }, {
                        "value": "1234",
                        "subroutine": "sr_api_call"
                    }
                ]
            }
        }, {
            "remap_fields": {
                "f1_---_f2": {
                    "_type": "int"
                }
            }
        }]
        subroutines = [{
            "sr_view_screen": [{
                "flatten": {"delimiter": "__"}
            }]
        }, {
            "sr_api_call": [{
                "flatten": {"delimiter": "_---_"}
            }]
        }]

        result = self.transform.transform(input, chain, subroutines)

        self.assertDictEqual(result['data'][0], expected)

    def test_process_by_field_value_nested_no_cast(self):
        input = {
            "event_name": "api_call",
            "f1": {
                "f2": 1234.56
            }
        }
        expected = {
            "event_name": "api_call",
            "f1_---_f2": 1234.56
        }
        chain = [{
            "process_by_field_value": {
                "field": {
                    "f1": "f2"
                },
                "values": [
                    {
                    "value": 5678,
                    "subroutine": "sr_view_screen"
                    }, {
                        "value": 1234.56,
                        "subroutine": "sr_api_call"
                    }
                ]
            }
        }]
        subroutines = [{
            "sr_view_screen": [{
                "flatten": {"delimiter": "__"}
            }]
        }, {
            "sr_api_call": [{
                "flatten": {"delimiter": "_---_"}
            }]
        }]

        result = self.transform.transform(input, chain, subroutines)

        self.assertDictEqual(result['data'][0], expected)

    def test_filter_subset_blacklist(self):
        input = {
            "f1": 0,
            "f2": 1,
            "f3": "a",
            "f4": "b"
        }
        subset = ["f1", "f3"]
        expected = {
            "f2": 1,
            "f4": "b"
        }

        chain = [{
            "filter_subset_blacklist": subset
        }]

        result = self.transform.transform(input, chain)

        self.assertDictEqual(result['data'][0], expected)

    def test_unnest_to_rows_null(self):
        input = {
            "f1": 1,
            "f2": [1,2,3,4],
            "f4": {"a": "b"},
            "f5": None
        }
        expected = {
            "f1": 1,
            "f2": [1,2,3,4],
            "f4": {"a": "b"},
            "f5": None
        }

        chain = [{
            "unnest_to_row": {"f5"}
        }]

        result = self.transform.transform(input, chain)

        self.assertDictEqual(result['data'][0], expected)

    def test_unnest_to_rows_nested_null(self):
        input = {
            "f1": 1,
            "f2": [1,2,3,4],
            "f4": {"a": "b"},
            "f5": {
                "a": None,
                "b": [5,6,7,8]
            }
        }
        expected = {
            "f1": 1,
            "f2": [1,2,3,4],
            "f4": {"a": "b"},
            "f5": {
                "a": None,
                "b": [5,6,7,8]
            }
        }

        chain = [{
            "unnest_to_row": {"f5": {"a"}}
        }]

        result = self.transform.transform(input, chain)

        self.assertDictEqual(result['data'][0], expected)

    def test_unnest_to_rows(self):
        input = {
            "f1": 1,
            "f2": [1,2,3,4],
            "f4": {"a": "b"},
            "f5": [
                {"item": 1, "quantity": 1},
                {"item": 2, "quantity": 2},
                {"item": 3, "quantity": 3}
            ]
        }
        expected = [{
            "f1": 1,
            "f2": [1,2,3,4],
            "f4": {"a": "b"},
            "f5": {"item": 1, "quantity": 1}
        },
        {
            "f1": 1,
            "f2": [1,2,3,4],
            "f4": {"a": "b"},
            "f5": {"item": 2, "quantity": 2}
        },
        {
            "f1": 1,
            "f2": [1,2,3,4],
            "f4": {"a": "b"},
            "f5": {"item": 3, "quantity": 3}
        }]

        chain = [{
            "unnest_to_row": {"f5"}
        }]

        result = self.transform.transform(input, chain)

        self.assertListEqual(result['data'], expected)

    def test_unnest_to_rows_single(self):
        input = {
            "f1": 1,
            "f2": [1,2,3,4],
            "f4": {"a": "b"},
            "f5": [
                {"item": 1, "quantity": 1}
            ]
        }
        expected = {
            "f1": 1,
            "f2": [1,2,3,4],
            "f4": {"a": "b"},
            "f5": {"item": 1, "quantity": 1}
        }

        chain = [{
            "unnest_to_row": {"f5"}
        }]

        result = self.transform.transform(input, chain)

        self.assertDictEqual(result['data'][0], expected)

    def test_unnest_to_rows_nested_fields(self):
        input = {
            "f1": 1,
            "f2": [1,2,3,4],
            "f4": {"a": "b"},
            "f5": [
                {"item": {
                    "field": [{
                        "x": 1,
                        "y": 3
                    }, {
                        "x": 2,
                        "y": 4
                    }]
                }}
            ]
        }
        expected = [{
            "f1": 1,
            "f2": [1,2,3,4],
            "f4": {"a": "b"},
            "f5": [{"item": {"field": {"x": 1, "y": 3}}}]
        }, {
            "f1": 1,
            "f2": [1,2,3,4],
            "f4": {"a": "b"},
            "f5": [{"item": {"field": {"x": 2, "y": 4}}}]
        }]

        chain = [{
            "unnest_to_row": {"f5": [{"item": {"field"}}]}
        }]

        result = self.transform.transform(input, chain)

        self.assertListEqual(result['data'], expected)

    def test_lift_value(self):
        input = {
            "event_params": {
                "key": "status",
                "value": {
                    "integer": 200
                }
            }
        }
        expected = {
            "event_params": {
                "key": "status",
                "value": 200
            }
        }
        chain = [{
            "lift_value": {
                "event_params": {
                    "value": {
                        "_lift": "integer"
                    }
                }
            }
        }]

        result = self.transform.transform(input, chain)

        self.assertDictEqual(result['data'][0], expected)

    def test_lift_value_nested(self):
        input = {
            "event_params": [
                {
                    "key": "status",
                    "value": {
                        "integer": 200
                    }
                }
            ]
        }
        expected = {
            "event_params": [
                {
                    "key": "status",
                    "value": 200
                }
            ]
        }
        chain = [{
            "lift_value": {
                "event_params": [{
                    "value": {
                        "_lift": "integer"
                    }
                }]
            }
        }]

        result = self.transform.transform(input, chain)

        self.assertDictEqual(result['data'][0], expected)

    def test_chain_unnesting(self):
        input = {
            "f1": 1,
            "f2": [1,2,3,4],
            "f4": {"a": "b"},
            "f5": [
                {"item": {
                    "field": [{
                        "x": 1,
                        "y": 3
                    }, {
                        "x": 2,
                        "y": 4
                    }]
                }}
            ]
        }
        _expected = [{
            "f1": 1,
            "f2": [1,2,3,4],
            "f5": [{"item": {"field": 3}}]
        }, {
            "f1": 1,
            "f2": [1,2,3,4],
            "f5": [{"item": {"field": 4}}]
        }]

        chain = [{
            "unnest_to_row": {"f5": [{"item": {"field"}}]}
        }, {
            "lift_value": { "f5": [{"item": {"field": {"_lift": "y"}}}]}
        }, {
            "filter_subset": ["f1", "f2", "f5"]
        }]

        result = self.transform.transform(input, chain)

        self.assertListEqual(result['data'], _expected)

    def test_sz(self):
        input = {"app_info": {"first_installation_time": "2021-06-16T19:23:48.327Z", "id": "com.mymtnnextgen", "install_referrer": "utm_source=google-play&utm_medium=organic", "installation_id": "e2de879d-03b0-425a-8bc8-b4f58ae10786", "last_update_time": "2021-07-31T19:14:55.227Z", "version": "1.0.8"}, "app_performance": {"battery_low_power_mode": False, "battery_percentage": 0.3799999952316284, "battery_state": "CHARGING", "data_down_kb": 0, "data_up_kb": 0}, "cart": [], "cart_id": "af5e32edfd42daa142b1162a740e28b179548da69ae1a5714ee3386dd02e6e32", "device": {}, "event_date": "2021-08-22", "event_name": "view_screen", "event_params": [{"key": "feature", "value": {"string": "promo"}}, {"key": "screen", "value": {"string": "promo"}}, {"key": "view_state", "value": {"string": "empty"}}], "event_timestamp": 1629613598113942.0, "mtn_account": {}, "network": {"carrier": "Eswatini Mobile", "carrier_iso_country_code": "sz", "cellular_generation": "CELLULAR_4G", "mobile_country_code": "653", "mobile_network_code": "10", "network_state_type": "CELLULAR"}, "session": {"id": "18915c5532c3bfb79bd2c4b4ebbcb2248d28d354bf9ca8709a0e4b63c51c4c0e", "start_time": 1629613466340000, "utm": []}, "user_country": "SZ", "user_id": "2c630b69dc2e0c179bf7651f5520c628677e94c816e7f3bda04a1500c4b5deb8", "user_properties": []}
        expected = {
            "cart": [], 
            "cart_id": "af5e32edfd42daa142b1162a740e28b179548da69ae1a5714ee3386dd02e6e32",
            "device": {}, 
            "event": "view_screen",
            "UNIX": 1629613598113942.0
        }
        chain = [{
            "filter_subset": ["event_name", "event_timestamp", "cart", "cart_id", "device"]
        }, {
            "remap_fields": {
                "event_name": {"_name": "event"},
                "event_timestamp": {"_name": "UNIX"}
            }
        }, {
            "flatten": {
                "delimiter": "_-_",
                "exclude": []
            }
        }]

        result = self.transform.transform(input, chain)

        self.assertDictEqual(result['data'][0], expected)

    def test_remap_empty(self):
        input = {"cart": [], "cart_id": "xxx1234", "device": {}, "event_name": "view_screen", "timestamp": 12132435.04}
        expected = {"cart": [], "cart_id": "xxx1234", "device": {}, "event": "view_screen", "UNIX": 12132435.04}
        chain = [{
            "remap_fields": {
                "event_name": {"_name": "event"},
                "timestamp": {"_name": "UNIX"}
            }
        }]

        result = self.transform.transform(input, chain)

        self.assertDictEqual(result['data'][0], expected)

    def test_set_target_by_field_value(self):
        input = {"cart": [], "cart_id": "xxx1234", "device": {}, "event_name": "view_screen", "timestamp": 12132435.04}
        expected = {"data": [{"cart": [], "cart_id": "xxx1234", "device": {}, "event": "view_screen", "UNIX": 12132435.04}], "targets": ["/projects/mkfnsd/topic/fnii20hf2fn"]}
        chain = [{
            "remap_fields": {
                "event_name": {"_name": "event"},
                "timestamp": {"_name": "UNIX"}
            }
        }, {
            "set_target_by_field_value": {
                "field": "event",
                "values": [{
                    "value": "view_screen",
                    "target": "/projects/mkfnsd/topic/fnii20hf2fn"
                }]
            }
        }]

        result = self.transform.transform(input, chain)

        self.assertDictEqual(result, expected)

    def test_set_target_by_field_value_multiple_items(self):
        input = [
            {"cart": [], "cart_id": "xxx1234", "device": {}, "event_name": "view_screen", "timestamp": 12132435.04},
            {"cart": [], "cart_id": "x5678", "device": {}, "event_name": "some_other", "timestamp": 5566.43}
        ]
        expected = {
            "data": [
                {"cart": [], "cart_id": "xxx1234", "device": {}, "event": "view_screen", "UNIX": 12132435.04},
                {"cart": [], "cart_id": "x5678", "device": {}, "event": "some_other", "UNIX": 5566.43}
            ], "targets": ["/projects/mkfnsd/topic/fnii20hf2fn", None]
        }
        chain = [{
            "remap_fields": {
                "event_name": {"_name": "event"},
                "timestamp": {"_name": "UNIX"}
            }
        }, {
            "set_target_by_field_value": {
                "field": "event",
                "values": [{
                    "value": "view_screen",
                    "target": "/projects/mkfnsd/topic/fnii20hf2fn"
                }, {
                    "value": "*"
                }]
            }
        }]

        result = self.transform.transform(input, chain)

        # z = zip(result['data'], result['targets'])

        self.assertDictEqual(result, expected)

    def test_key_value_collapse(self):
        input = {"event_params": [{"key": "api_name", "value": "share"}]}
        chain = [{
            "key_value_collapse": {
                "key_field": {
                    "event_params": [
                        {"key"}
                    ]
                },
                "value_field": {
                    "event_params": [
                        {"value"}
                    ]
                }
            }
        }]
        expected = {"event_params": [{"api_name": "share"}]}

        result = self.transform.transform(input, chain)

        self.assertDictEqual(result['data'][0], expected)

    def test_key_value_collapse_target(self):
        input = {
            "event_params": [{
                "key": "api_name", 
                "value": "share"
            }]
        }
        chain = [{
            "key_value_collapse": {
                "key_field": {
                    "event_params": [
                        {"key"}
                    ]
                },
                "value_field": {
                    "event_params": [
                        {"value"}
                    ]
                },
                "target_field": "test_field"
            }
        }]
        expected = {
            "event_params": [{}],
            "test_field": {"api_name": "share"}
        }

        result = self.transform.transform(input, chain)

        self.assertDictEqual(result['data'][0], expected)

    def test_key_value_collapse_target(self):
        input = {
            "event_params": [{
                "key": "api_name", 
                "value": "share"
            }]
        }
        chain = [{
            "key_value_collapse": {
                "key_field": {
                    "event_params": [{
                        "key"
                    }]
                },
                "value_field": {
                    "event_params": [
                        {"value"}
                    ]
                },
                "target_field": "*"
            }
        }]
        expected = {
            "event_params": [{}],
            "api_name": "share"
        }

        result = self.transform.transform(input, chain)

        self.assertDictEqual(result['data'][0], expected)

    def test_key_value_collapse_target_multiple_root(self):
        input = {
            "event_params": [{
                "key": "api_name", 
                "value": "share"
            }, {
                "key": "api_response", 
                "value": 200
            }]
        }
        chain = [{
            "key_value_collapse": {
                "key_field": {
                    "event_params": [{
                        "key"
                    }]
                },
                "value_field": {
                    "event_params": [
                        {"value"}
                    ]
                },
                "target_field": "*"
            }
        }]
        expected = {
            "event_params": [{}, {}],
            "api_name": "share",
            "api_response": 200
        }

        result = self.transform.transform(input, chain)

        self.assertDictEqual(result['data'][0], expected)

    def test_key_value_collapse_target_multiple_deep(self):
        input = {
            "event_params": [{
                "key": "api_name", 
                "value": "share"
            }, {
                "key": "api_response", 
                "value": 200
            }]
        }
        chain = [{
            "key_value_collapse": {
                "key_field": {
                    "event_params": [{
                        "key"
                    }]
                },
                "value_field": {
                    "event_params": [
                        {"value"}
                    ]
                },
                "target_field": {"x": {"y"}}
            }
        }]
        expected = {
            "event_params": [{}, {}],
            "x": {
                "y": {
                    "api_name": "share",
                    "api_response": 200
                }
            }
        }

        result = self.transform.transform(input, chain)

        self.assertDictEqual(result['data'][0], expected)

    def test_process_by_field_key(self):
        input = {
            "event_params": [{
                "integer": 200,
                "string": "test"
            }]
        }
        expected = {
            "event_params__0__integer": 200,
            "event_params__0__string": "test"
        }
        chain = [{
            "process_by_field_key": {
                "field": "event_params",
                "values": [{
                    "value": "string",
                    "subroutine": "sr_view_screen"
                }]
            }
        }]

        subroutines = [{
            "sr_view_screen": [{
                "flatten": {
                    "delimiter": "__",
                    "exclude": []
                }
            }]
        }]

        result = self.transform.transform(input, chain, subroutines)

        self.assertDictEqual(result['data'][0], expected)

    def test_flatten_exclude(self):
        input = {
            "field": {
                "sub-field1": 1,
                "sub-field2": 2
            },
            "dont-flatten": {
                "sub-field1": 3,
                "sub-field2": 4
            },
            "field3": {
                "sub-field1": 5,
                "sub-field2": 6,
                "sub-list1": [{
                    "sub-field001": 10,
                    "sub-field002": 11,
                }, {
                    "sub-field003": 12,
                }]
            }
        }

        chain = [{
            "flatten": {"delimiter": "__", "exclude": ["dont-flatten"]}
        }]

        expected = {
            "field__sub-field1": 1,
            "field__sub-field2": 2,
            "dont-flatten": {
                "sub-field1": 3,
                "sub-field2": 4
            },
            "field3__sub-field1": 5,
            "field3__sub-field2": 6,
            "field3__sub-list1__0__sub-field001": 10,
            "field3__sub-list1__0__sub-field002": 11,
            "field3__sub-list1__1__sub-field003": 12
        }

        result = self.transform.transform(input, chain)

        self.assertDictEqual(result['data'][0], expected)

    def test_flatten_include(self):
        input = {
            "field": {
                "sub-field1": 1,
                "sub-field2": 2
            },
            "dont-flatten": {
                "sub-field1": 3,
                "sub-field2": 4
            },
            "field3": {
                "sub-field1": 5,
                "sub-field2": 6,
                "sub-list1": [{
                    "sub-field001": 10,
                    "sub-field002": 11,
                }, {
                    "sub-field003": 12,
                }]
            }
        }

        chain = [{
            "flatten": {"delimiter": "__", "exclude": ["dont-flatten"], "include": ["field3"]}
        }]

        expected = {
            "field": {
                "sub-field1": 1,
                "sub-field2": 2
            },
            "dont-flatten": {
                "sub-field1": 3,
                "sub-field2": 4
            },
            "field3__sub-field1": 5,
            "field3__sub-field2": 6,
            "field3__sub-list1__0__sub-field001": 10,
            "field3__sub-list1__0__sub-field002": 11,
            "field3__sub-list1__1__sub-field003": 12
        }

        result = self.transform.transform(input, chain)
        
        self.assertDictEqual(result['data'][0], expected)


if __name__ == "__main__":
    unittest.main()