from metatransform import MetaTransform
import json

transform = MetaTransform()

data = {
    'id': '1234abc',
    'params': [{
        'key': 'lift_to_root',
        'value': {'int': 1234}
    }, {
        'key': 'rename_key',
        'value': 5678
    }],
    'cast_to_string': {
        '_dict': {'a': 'b', 'c': 'd'},
        '_list': ['a','b','c','d'],
        '_int': 1000,
        '_bool': False
    },
    'filter_this_out': '...',
    'last': 12
}

chain = [ 
    {
        "lift_value": {
            "params": [{
                "value": {
                    "_lift": "integer"
                }
            }]
        }
    }, {
        "key_value_collapse": {
            "key_field": {
                "params": [
                    "key"
                ]
            },
            "value_field": {
                "params": [
                    "value"
                ]
            },
            "target_field": "*"
        }
    }, {
        "cast_string": {"cast_to_string": "_dict"}
    }, {
        "cast_string": {"cast_to_string": "_list"}
    }, {
        "cast_string": {"cast_to_string": "_int"}
    }, {
        "cast_string": {"cast_to_string": "_bool"}
    }, {
        "filter_subset_blacklist": ["filter_this_out"]
    }
]

chain = [
        {
            "filter_subset_blacklist": ["filter_this_out", "last"]
        }, 
        {
            "key_value_collapse": {
                "key_field": {
                    "params": [
                        "key"
                    ]
                },
                "value_field": {
                    "params": [
                        "value"
                    ]
                },
                "target_field": "*"
            }
        },
        {
            "filter_subset_blacklist": ["params"]
        },
        {
            "remap_fields": {
                "cast_to_string": {
                    "_dict": {
                        "_type": "string"
                    },
                    "_list": {
                        "_type": "string"
                    },
                    "_int": {
                        "_type": "string"
                    },
                    "_bool": {
                        "_type": "string"
                    }
                },
                "rename_key": {
                    "_name": "new_key"
                }
            }
        }, 
        {
            "lift_value": {
                "lift_to_root": {
                    "_lift": "int"
                }
            }
        },
    ]

result = transform.transform(data, chain)

print(json.dumps(result, indent=4))