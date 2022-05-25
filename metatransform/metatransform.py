from applyrecursive import ApplyRecursive
from .transforms import MetaTransformTransforms

class MetaTransform(MetaTransformTransforms):
    """
    Utility class for transforming data objects
    """

    def __init__(self, transforms:list=[], routines:dict={}) -> None:
        self.transforms = transforms
        self.routines = routines

    def _get_func(self, fn, run = True, *args, **kwargs):
        func = getattr(self, fn, None)
        if run:
            try: func(*args, **kwargs)
            except Exception as e: pass
        else:
            return func
    
    def _chain(self, transforms:list, data:list):

        for transform in transforms:
            
            _function = transform.get('function', None)
            
            if _function in self.routines:
                self._chain(self.routines[_function], data)
                continue

            try:
                if isinstance(data, list):
                    for idx, item in enumerate(data): 
                        self._map(function=_function, data=data[idx], transform=transform)
                else:
                    self._map(function=_function, data=data, transform=transform)
            except Exception as e: pass
                # print(f'chain error: {str(e)} {type(e)}; {_function}')

    def _map(self, *args, **kwargs):
        _f = kwargs.get('function')
        _d = kwargs.get('data')
        _t = kwargs.get('transform', {})
        _m = _t.get('map', {})
        _o = _t.get('options', {})

        _f_callable = self._get_func(_f, run=False) if not callable(_f) else _f

        if _m:
            _applyrecursive = ApplyRecursive(_f_callable, args, _o, 'data')
            _applyrecursive.apply(_m, '__modify', _d, _o.get('create', False))
        else:
            if _f in self.routines:
                self._chain(self.routines[_f], _d)
            else:
                try: _f_callable(data=_d, options=_o)
                except Exception as e: pass
                    # print(f'failed on {_f}; {str(e)}')
                    # print(getattr(self, _f))

    def run(self, data:list):
        """
        `data`: a `list` of objects to transform
        """

        if not isinstance(data, list):
            raise Exception('data must be a list')

        if not isinstance(self.transforms, list):
            raise Exception('data must be a list')

        _obj = [{'transforms': self.transforms, 'data': record} for record in data] if isinstance(data, list) else [{'transforms': self.transforms, 'data': data}]

        for x in _obj:
            self._chain(x['transforms'], x['data'])