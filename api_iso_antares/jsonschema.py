from typing import cast, List, Optional

from api_iso_antares.custom_types import JSON, SUB_JSON


class JsonSchema:
    def __init__(self, data: JSON) -> None:
        self.data = data

    def get_properties(self) -> List[str]:

        return [
            key for key in self.data["properties"].keys() if not (key == "$id")
        ]

    def get_child(self, key: Optional[str] = None) -> "JsonSchema":
        data: JSON
        if key is None:
            data = self.data["items"]
        else:
            data = self.data["properties"][key]
        return JsonSchema(data)

    def get_additional_properties(self) -> "JsonSchema":
        data = self.data["additionalProperties"]
        return JsonSchema(data)

    def get_metadata(self) -> Optional[JSON]:
        return self.data.get("rte-metadata", None)

    def get_metadata_element(self, key: str) -> SUB_JSON:
        metadata = self.get_metadata()
        element: SUB_JSON = None
        if metadata is not None:
            element = metadata.get(key, None)
        return element

    def get_filename(self) -> Optional[str]:
        return cast(str, self.get_metadata_element("filename"))

    def get_strategy(self) -> Optional[str]:
        return cast(Optional[str], self.get_metadata_element("strategy"))

    def get_type(self) -> str:
        return cast(str, self.data["type"])

    def is_array(self) -> bool:
        return self.get_type() == "array"

    def is_object(self) -> bool:
        return self.get_type() == "object"