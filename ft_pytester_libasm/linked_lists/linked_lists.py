"""
This module provides tools for working with chained lists.
"""

from typing import List
from ctypes import Structure, c_void_p, pointer, POINTER, cast
import ctypes


# TODO: Make it explicitly abstract.
class BaseLinkedList(Structure):
    """
    LinkedList emulates a C linked list defined as:

    struct s_list
    {
        void                *data;
        struct s_list       *next;
    };
    """

    def data_repr(self) -> str:
        raise NotImplementedError()

    def single_node_repr(self) -> str:
        next = f"{self.next}" if self.next else "NULL"
        return (
            f"Data location: {self.data}.\n"
            f"Data: {self.data_repr()}.\n"
            f"Next node address: {next}."
        )

    # TODO: How to avoid the POINTER(self.__class__) that would make the type
    #       constant through all the linked list?
    #       Maybe give up these methods for the base class and only use them
    #       in specific subclasses?
    def full_linked_list_repr(self) -> str:
        node: BaseLinkedList = self
        all_nodes_repr: List[str] = [
            self.single_node_repr(),
        ]
        while node.next:
            node = cast(node.next, POINTER(self.__class__))[0]
            all_nodes_repr.append(node.single_node_repr())
        return "\n\n".join(
            f"Node #{i}:\n" + r for i, r in enumerate(all_nodes_repr)
        )

    def __repr__(self) -> str:
        return self.full_linked_list_repr()


BaseLinkedList._fields_ = [
    ("data", c_void_p),
    ("next", POINTER(BaseLinkedList)),
]


class IntLinkedList(BaseLinkedList):
    """
    This simple BaseLinkedList subclass handles integers as data.
    """

    # Cast(
    #     cast(
    #         node_1.next, POINTER(IntLinkedList))[0].data, POINTER(
    #             ctypes.c_int
    #         )
    # )[0],

    def data_repr(self) -> str:
        return str(cast(self.data, POINTER(ctypes.c_int))[0])

    def __eq__(self, other) -> bool:
        if (self.next is None) == (other.next is None):
            return (
                ctypes.c_int(self.data[0]) == ctypes.c_int(other.data[0])
                and self.next[0] == other.next[0]
            )
        return False


def build_int_linked_list(integers_list: List[int]):
    node_p = POINTER(IntLinkedList)()
    for i in integers_list[::-1]:
        node: IntLinkedList = IntLinkedList(
            data=cast(pointer(ctypes.c_int(i)), c_void_p),
            next=cast(node_p, POINTER(BaseLinkedList)),
        )
        node_p = pointer(node)
    return node_p
