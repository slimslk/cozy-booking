from typing import Any

from apps.errors.common_errors import NoContentFoundError, NoDataToUpdateError


def check_content_helper(content: Any):
    if not content:
        raise NoContentFoundError()


def check_and_update_entity_with_new_data_helper(entity: Any, updated_data: dict[str, Any]) -> Any:
    is_updated = False
    for key, value in updated_data.items():
        if getattr(entity, key) != value:
            setattr(entity, key, value)
            is_updated = True
    if not is_updated:
        raise NoDataToUpdateError()
    return entity


if __name__ == '__main__':
    pass
