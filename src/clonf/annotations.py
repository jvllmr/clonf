from __future__ import annotations
from dataclasses import dataclass, field
import typing as t
from pydantic import BaseModel
from pydantic.fields import FieldInfo


# https://github.com/pydantic/pydantic/discussions/5970
def is_pydantic_model_annotation(ann: type[t.Any]) -> bool:
    return hasattr(ann, "mro") and BaseModel in ann.mro()


@dataclass
class ClonfAnnotation:
    name: str | ellipsis = field(default=...)
    description: str | None = field(default=None)
    _type: t.Any | None = field(default=None, init=False)
    _field_info: FieldInfo | None = field(default=None, init=False)
    multiple: bool = field(default=False)
    _sub_path: tuple[str, type[BaseModel]] | None = field(default=None, init=False)

    @property
    def kwarg(self) -> str:
        assert self.name is not Ellipsis, "Name was not initialized"
        return self.name.replace("-", "_")

    @property
    def unprefixed_kwarg(self) -> str:
        kwarg = self.kwarg
        if self._sub_path is None:
            return kwarg
        prefix = self._sub_path[0]

        return kwarg[len(prefix) + 1 :]


@dataclass
class CliArgument(ClonfAnnotation):
    default: t.Any = field(default=...)


@dataclass
class CliOption(ClonfAnnotation):
    default: t.Any = field(default=...)
    prefix: str = field(default="--")
    is_flag: bool = field(default=False)
