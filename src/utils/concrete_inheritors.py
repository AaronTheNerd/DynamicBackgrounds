import inspect
from typing import Any, Optional, TypeVar

from configs import ObjectConfigs

T = TypeVar("T")


def concrete_inheritors(cls: T) -> dict[str, T]:
    subclasses = {}
    work = [cls]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child.__name__ not in subclasses:
                work.append(child)
                if not inspect.isabstract(child):
                    subclasses[child.__name__] = child
    return subclasses


def get_object(cls: type[T], configs: ObjectConfigs | dict[str, Any]) -> T:
    if not isinstance(configs, ObjectConfigs):
        configs = ObjectConfigs(**configs)
    subclasses = concrete_inheritors(cls)
    return subclasses[configs.type].from_json(**configs.kwargs)
