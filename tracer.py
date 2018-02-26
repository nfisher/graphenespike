import flask_opentracing as ot
import jaeger_client as jaeger
import graphql.type.definition as definition

def initialize_tracer():
    """
    initialize_tracer
    """
    config = jaeger.Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name='swapi',
    )
    return config.initialize_tracer()

tracer = None

def instance(app=None):
    global tracer
    if tracer is None:
        tracer = ot.FlaskTracer(initialize_tracer, True, app)
    return tracer


class ResolveInfoProxy:
    def __init__(self, info, tracer, name):
        self._info = info
        self._tracer = tracer
        self._name = name
        self._parent = None

    def __getattr__(self, item):
       result = getattr(self._info, item)
       return result

def operation_name(parent_type, field_name):
    if parent_type is None:
        return field_name

    return "{parent_type}.{field_name}".format(
                parent_type=parent_type,
                field_name=field_name,
            )

def middleware(next, root, info, **args):
    """
    tracer_middleware adds trace spans to each field resolver call.
    """
    parent_type = None
    if root and hasattr(root, '_meta'):
        parent_type = root._meta.name

    if isinstance(info.return_type, definition.GraphQLScalarType):
        return_value = next(root, info, **args)
    else:
        name = operation_name(parent_type, info.field_name)
        return_value = next(root, ResolveInfoProxy(info, instance(), name), **args)

    return return_value
