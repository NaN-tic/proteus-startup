from proteus import Model
from functools import wraps


def create_model(model_name):
    '''
    Decorator that creates a tryton model

    It decorates a function that when each arg is the value of the field.
    The function is called before initialitzing the record. It can return:
        - The created instance
        - A dict which values are used to override the initial args.
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cls = Model.get(model_name)
            values = kwargs.copy()
            new_values = func(*args, **kwargs)
            if new_values and isinstance(new_values, cls):
                return new_values
            if new_values:
                values.update(new_values)
            model = cls()
            for field, value in values.items():
                if field in cls._fields:
                    if not value:
                        continue
                    definition = cls._fields[field]
                    if definition['type'] in ('one2many', 'many2many'):
                        relation = Model.get(definition['relation'],
                            cls._config)
                        # Rebrowse to avoid parent errors
                        for v in value:
                            if v.id and v.id > 0:
                                v = relation(v.id)
                            getattr(model, field).append(v)
                    else:
                        setattr(model, field, value)

            return model
        return wrapper
    return decorator
