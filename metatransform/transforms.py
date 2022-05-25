from random import randint, choice

class MetaTransformTransforms():
    def _parse_kwargs(self, **kwargs):
        data = kwargs.get('data', {})
        options = kwargs.get('options', {})
        return data, options

    def whatver(self, *args, **kwargs):
        _d, _o = self._parse_kwargs(**kwargs)
        _d['new_field'] = _o.get('text', 'HELLO')

    def cc(self, *args, **kwargs):
        return randint(999, 8000)

    def deep(self, *args, **kwargs):
        _d, _o = self._parse_kwargs(**kwargs)
        # if isinstance(_d, dict):
        #     print(_d)
        _d['y']['c']['g'] = choice(['first', 'second', 'third'])

    def rrrr(self, *args, **kwargs):
        _d, _o = self._parse_kwargs(**kwargs)
        _d['routine'] = 'ITS A ME'

    def flatten(self, *args, **kwargs):
        _d, _o = self._parse_kwargs(**kwargs)

        if isinstance(_d, list):
            return ",".join((str(value) for value in _d))
        if isinstance(_d, dict):
            return ";".join([f'{k}:{v}' for k, v in _d.items()])        
        
        return _d