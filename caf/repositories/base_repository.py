"""Base repository for CAF application."""

from typing import TYPE_CHECKING, Generic, Protocol, TypeVar

if TYPE_CHECKING:
    from caf.models.instruction import Instruction  # noqa: F401
    from caf.models.variant import Variant  # noqa: F401
    from caf.models.version import Version  # noqa: F401


class Identifiable(Protocol):
    """Protocol for objects with an id attribute."""

    id: str


class RepositoryProtocol[T](Protocol):
    """Protocol defining the common repository interface."""

    def save(self, item: T) -> None: ...
    def get_by_id(self, item_id: str) -> T: ...
    def get_all(self) -> list[T]: ...
    def delete(self, item_id: str) -> None: ...


class InstructionRepositoryProtocol(RepositoryProtocol["Instruction"], Protocol):
    """Extended protocol for instruction repositories."""

    pass


class VersionRepositoryProtocol(RepositoryProtocol["Version"], Protocol):
    """Extended protocol for version repositories."""

    def get_by_instruction_id(self, instruction_id: str) -> list["Version"]: ...


class VariantRepositoryProtocol(RepositoryProtocol["Variant"], Protocol):
    """Extended protocol for variant repositories."""

    def get_by_version_id(self, version_id: str) -> list["Variant"]: ...


T = TypeVar("T", bound=Identifiable)


class BaseRepository(Generic[T], RepositoryProtocol[T]):  # noqa: UP046
    """Base in-memory repository with common CRUD operations."""

    def __init__(self) -> None:
        """Initialize the repository."""
        self._items: dict[str, T] = {}
        self._order: list[str] = []

    def save(self, item: T) -> None:
        """Save an item to the repository.

        Args:
            item: Object to save. Must have an 'id' attribute.
        """
        item_id = item.id
        if item_id not in self._items:
            self._order.append(item_id)
        self._items[item_id] = item

    def get_by_id(self, item_id: str) -> T:
        """Retrieve an item by ID.

        Args:
            item_id: ID of the item to retrieve.

        Returns:
            Object with the given ID.

        Raises:
            ValueError: If item with given ID does not exist.
        """
        if item_id not in self._items:
            raise ValueError(f"Item with id '{item_id}' not found")
        return self._items[item_id]

    def get_all(self) -> list[T]:
        """Retrieve all items in insertion order.

        Returns:
            List of all objects.
        """
        return [self._items[id_] for id_ in self._order]

    def delete(self, item_id: str) -> None:
        """Delete an item by ID.

        Args:
            item_id: ID of the item to delete.

        Raises:
            ValueError: If item with given ID does not exist.
        """
        if item_id not in self._items:
            raise ValueError(f"Item with id '{item_id}' not found")
        del self._items[item_id]
        self._order.remove(item_id)
