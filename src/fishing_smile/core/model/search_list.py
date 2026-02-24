from typing import Any, get_args as get_type_args
from collections.abc import Mapping

from pydantic_core import CoreSchema, core_schema
from pydantic import GetCoreSchemaHandler


class SearchList[T](list[T]):
    """List, but with extra methods for searching items"""

    @staticmethod
    def match(item: T, conditions: dict) -> bool:
        match item:
            case Mapping():
                try:
                    for key, value in conditions.items():
                        if item[key] != value:
                            return False
                except KeyError:
                    return False
            case _:
                try:
                    for key, value in conditions.items():
                        if getattr(item, key) != value:
                            return False
                except AttributeError:
                    return False
        return True

    def first(self, **conditions) -> T:
        """Find the first item with keys/properties matching given conditions."""
        for item in self:
            if self.match(item, conditions):
                return item

        raise ValueError(f'No item matching criteria: {conditions}')

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        type_args = get_type_args(source_type)
        item_type = type_args[0] if type_args else Any
        return core_schema.no_info_after_validator_function(
            cls,
            handler.generate_schema(list[item_type]),
        )
