#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
# Meta info

Author: Nelson Brochado

Created: 01/07/2015

Updated: 11/03/2017

# Description

This module contains currently the classes `BHNode`, which is a class to represent nodes of heaps,
the class `BinaryHeap` and a function which returns a pretty string representation of a heap passed as parameter.

## Public interface

- add(x): O(log(n))
- search(x): O(n)
- delete(x): O(n)
- replace(x, y): O(n)
- size(): O(1)
- is_empty(): O(1)
- clear(): O(1)
- merge(o): O(n + m)

searches for object x in the heap; if object x exists, it returns the value associated with it, otherwise it returns -1

# References

- [http://www.math.clemson.edu/~warner/M865/HeapDelete.html](http://www.math.clemson.edu/~warner/M865/HeapDelete.html)
- Slides by prof. A. Carzaniga
- Chapter 13 of [Introduction to Algorithms (3rd ed.)](https://mitpress.mit.edu/books/introduction-algorithms) by CLRS
- [NotImplementedError](https://docs.python.org/3/library/exceptions.html#NotImplementedError)
- [How do I check if an object is an instance of a given class or of a subclass of it?](http://effbot.org/pyfaq/how-do-i-check-if-an-object-is-an-instance-of-a-given-class-or-of-a-subclass-of-it.htm)
- [https://en.wikipedia.org/wiki/Heap_(data_structure)](https://en.wikipedia.org/wiki/Heap_(data_structure))
- [https://arxiv.org/pdf/1012.0956.pdf](https://arxiv.org/pdf/1012.0956.pdf)
"""

import io
import math
from abc import ABCMeta, abstractmethod

__all__ = ["BinaryHeap", "BHNode", "build_pretty_binary_heap"]


class BHNode:
    """All elements of heap objects are represented with objects of the class BHNode."""

    def __init__(self, key, value=None):
        """`key` is the priority used to heapify the heap,
        and it must be a non-None comparable value.
        `value` can be used for example for the name of the `BHNode` object."""
        if key is None:
            raise ValueError("key cannot be None.")
        self.key = key
        self.value = value if value is not None else self.key

    def __eq__(self, o):
        return self.key == o.key and self.value == o.value

    def __ne__(self, o):
        return not self.__eq__(o)

    def __le__(self, o):
        return self.key <= o.key

    def __ge__(self, o):
        return self.key >= o.key

    def __lt__(self, o):
        return not self.__ge__(o)

    def __gt__(self, o):
        return not self.__le__(o)

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return str(self.value) + " -> " + str(self.key)


class BinaryHeap(metaclass=ABCMeta):
    """Abstract class to represent binary heaps.

    `MinHeap`, `MaxHeap` and `MinMaxHeap` all derive from this class."""

    def __init__(self, ls=None):
        if ls is None:
            ls = []
        self.heap = BinaryHeap._create_list_of_heap_nodes(ls)
        self._build_heap()

    @staticmethod
    def _create_list_of_heap_nodes(ls: list) -> list:
        """Creates and returns a list of `BHNode` objects with the objects in `ls`.

        **Time complexity:** O(n)."""
        nodes = []
        for x in ls:
            # x represents also its priority.
            # Check if x is either an int or a float.
            if isinstance(x, (int, float)):
                nodes.append(BHNode(x))
            else:
                if len(x) != 2:
                    raise ValueError("x should be a tuple or list of 2 elements.")
                # x[0] := priority
                # x[1] := value associated with x[0]
                if x[0] is None or x[1] is None:
                    raise ValueError("keys or values cannot be None.")
                nodes.append(BHNode(key=x[0], value=x[1]))
        return nodes

    @abstractmethod
    def _push_down(self, i: int) -> None:
        """Classical _heapify_ operation for heaps."""
        pass

    @abstractmethod
    def _push_up(self, i: int) -> None:
        """Classical reverse-heapify operation for heaps."""
        pass

    def _build_heap(self) -> list:
        """Builds the heap data structure using Robert Floyd's heap construction algorithm.

        Floyd's algorithm is optimal as long as complexity is expressed in terms of sets of functions
        described via the asymptotic symbols O, Θ and Ω.
        Indeed, its linear complexity Θ(n), both in the worst and best case,
        cannot be improved as each object must be examined at least once.

        Floyd's algorithm was invented in 1964 as an improvement of the construction phase
        of the classical heap-sort algorithm introduced earlier that year by Williams J.W.J.

        **Time complexity:** Θ(n)."""
        if self.heap:
            for index in range(len(self.heap) // 2, -1, -1):
                self._push_down(index)

    def size(self) -> int:
        """Returns the size of this heaps.

        **Time complexity:** O(1)."""
        return len(self.heap)

    def is_empty(self) -> bool:
        """Returns `True` if this heap is empty.

        **Time complexity:** O(1)."""
        return self.size() == 0

    def clear(self) -> None:
        """Clears all nodes from this heap.
        This mean that if you call `is_empty`,
        it will return `True`.

        **Time complexity:** O(1)."""
        self.heap.clear()

    def add(self, x: object) -> None:
        """Adds object `x` to this heap.

        In practice, it places `x` at an available leaf,
        then "bubbles up" from there, in order to maintain the heap property.

        `x` can either be a key or a `BHNode` object.
        If it's a key, an `BHNode` is first created,
        whose key and value are equal to `x`.

        **Time complexity:** O(log n)."""
        if x is None:
            raise ValueError("x cannot be None.")
        if not isinstance(x, BHNode):
            x = BHNode(x)
        self.heap.append(x)
        if self.size() > 1:
            self._push_up(self.size() - 1)

    def search(self, x: object) -> int:
        """Searches for `x` in this heap, and, if present,
        returns its index, otherwise returns -1.

        `x` can either be a key or a `BHNode` object.
        If it's a key, an `BHNode` is first created,
        whose key and value are equal to `x`.

        **Time complexity:** O(n)."""
        if x is None:
            raise ValueError("x cannot be None.")
        if not isinstance(x, BHNode):
            x = BHNode(x)
        for i, node in enumerate(self.heap):
            if node == x:
                return i
        return -1

    def search_by_value(self, val: object) -> int:
        """Returns the index of the `BHNode` object with `value=val`.
        -1 is returned if no such a `BHNode` object exists.

        If `val` and the values in this heap are not comparable,
        the behaviour of this method is undefined.

        By construction, BHNode objects can't be initialized with None values,
        but that field could also be set manually after creation.

        **Time complexity:** O(n)."""
        for i, node in enumerate(self.heap):
            if node.value == val:
                return i
        return -1

    def contains(self, x: object) -> bool:
        """Returns `True`, if `x` is in this heap. `False` otherwise.

        `x` can either be a key or a `BHNode` object.
        If it's a key, an `BHNode` is first created,
        whose key and value are equal to `x`.

        **Time complexity:** O(n)."""
        return self.search(x) != -1

    @abstractmethod
    def delete(self, i: int) -> BHNode:
        """Deletes from self element at index `i` and returns it."""
        pass

    @abstractmethod
    def replace(self, i: int, x: object) -> BHNode:
        """Replaces the `BHNode` object at index `i` with `x`.

        `x` can either be a key or a `BHNode` object.
        If it's a key, an `BHNode` is first created,
        whose key and value are equal to `x`."""
        pass

    def merge(self, o) -> list:
        """Merges this heap with the `o` heap.

        Returns the `list` object representing internally the new merged heap.

        **Time complexity:** O(n + m).

        Time complexity analysis based on:
        [http://stackoverflow.com/a/29197855/3924118](http://stackoverflow.com/a/29197855/3924118)."""
        self.heap += o.heap
        self._build_heap()

    def _swap(self, i: int, j: int) -> None:
        """Swaps elements at indexes `i` and `j`, if they are valid indexes,
        otherwise an `IndexError` is raised.

        **Time complexity:** O(1)."""
        if self._is_good_index(i) and self._is_good_index(j):
            self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        else:
            raise IndexError("i or j are not valid indexes.")

    def _is_good_index(self, i: int) -> bool:
        """Returns `True` if `i` is valid index for `self.heap`,
        `False` otherwise.

        **Time complexity:** O(1)."""
        if not isinstance(i, int):
            raise TypeError("indexes can only be int.")
        return False if (i < 0 or i >= self.size()) else True

    def _parent_index(self, i: int) -> int:
        """Returns the parent's index of the node at index `i`.
        If `i = 0`, then -1 is returned, because the root has no parent.

        If `i` is not a valid index, an `IndexError` is raised.

        **Time complexity:** O(1)."""
        if not self._is_good_index(i):
            raise IndexError("i is not a valid index.")
        return -1 if i == 0 else (i - 1) // 2

    def _grandparent_index(self, i: int) -> int:
        """Returns the grandparent's index of the node at index `i`.

        -1 is returned either if `i` has not a parent or
        the parent of `i` does not have a parent.

        **Time complexity:** O(1)."""
        p = self._parent_index(i)
        return -1 if p == -1 else self._parent_index(p)

    def _left_index(self, i: int) -> int:
        """Returns the left child's index of the node at index `i`,
        if it exists, otherwise this function returns -1.

        If `i` is not a valid index, an `IndexError` is raised.

        **Time complexity:** O(1)."""
        if not self._is_good_index(i):
            raise IndexError("i is not a valid index.")
        left = i * 2 + 1
        return left if self._is_good_index(left) else -1

    def _right_index(self, i: int) -> int:
        """Returns the right child's index of the node at index `i`,
        if it exists, otherwise this function returns -1.

        If `i` is not a valid index, an `IndexError` is raised.

        **Time complexity:** O(1)."""
        if not self._is_good_index(i):
            raise IndexError("i is not a valid index.")
        right = i * 2 + 2
        return right if self._is_good_index(right) else -1

    def _has_children(self, i: int) -> bool:
        """Returns `True` if the node at index `i`
        has at least one child, `False` otherwise.

        **Time complexity:** O(1)."""
        if not self._is_good_index(i):
            raise IndexError("i is not a valid index.")
        return self._left_index(i) != -1 or self._right_index(i) != -1

    def _is_child(self, c: int, i: int) -> bool:
        """Returns `True` if `c` is a child of `i`. `False` otherwise.

        **Time complexity:** O(1)."""
        if not self._is_good_index(c) or not self._is_good_index(i):
            raise IndexError("i or c are not valid indexes.")
        return c == self._left_index(i) or c == self._right_index(i)

    def _is_grandchild(self, g: int, i: int) -> bool:
        """Returns `True` if `g` is a grandchild of `i`. `False` otherwise.

        **Time complexity:** O(1)."""
        l = self._left_index(i)
        if l == -1:
            assert self._right_index(i) == -1
            if not self._is_good_index(g):
                raise IndexError("g is not a valid index.")
            return False
        r = self._right_index(i)
        if r == -1:
            return self._is_child(g, l)
        else:
            return self._is_child(g, l) or self._is_child(g, r)

    def _is_parent(self, p: int, i: int) -> bool:
        """Returns `True` if `p` is the index of the parent
        of the node at `i`, `False` otherwise.

        **Time complexity:** O(1)."""
        if not self._is_good_index(p):
            raise IndexError("p is not a valid index.")
        return self._parent_index(i) == p

    def _is_grandparent(self, g: int, i: int) -> bool:
        """Returns `True` if `g` is the index of the grandparent
        of the node at `i`, `False` otherwise.

        **Time complexity:** O(1)."""
        if not self._is_good_index(g):
            raise IndexError("g is not a valid index.")
        p = self._parent_index(i)
        return False if p == -1 else self._is_parent(g, p)

    def _is_on_even_level(self, i: int) -> bool:
        """Returns `True` if node at index `i` is on a even-level,
        i.e., if `i` is on a level multiple of 2 (0, 2, 4, 6,...).
        If `i` is not a valid index, an `IndexError` is raised.

        **Time complexity:** O(int(math.log2(i + 1) % 2) == 0)."""
        if not self._is_good_index(i):
            raise IndexError("i is not a valid index.")
        return int(math.log2(i + 1) % 2) == 0

    def _is_on_odd_level(self, i: int) -> bool:
        """Returns `True` when self._is_on_even_level(i) returns `False`, and vice-versa."""
        return not self._is_on_even_level(i)

    def __str__(self) -> str:
        return str(self.heap)

    def __repr__(self) -> str:
        return build_pretty_binary_heap(self.heap)


def build_pretty_binary_heap(heap: list, total_width=36, fill=" ") -> str:
    """Returns a string (which can be printed) representing `heap` as a tree.

    Adapted for Python 3 from: [http://pymotw.com/2/heapq/](http://pymotw.com/2/heapq/).

    To increase/decrease the horizontal space between nodes,
    just increase/decrease the float number h_space.

    To increase/decrease the vertical space between nodes,
    just increase/decrease the integer number v_space.
    Note that v_space must be an integer.

    To change the length of the line under the heap,
    you can simply change the line_length variable."""
    if not isinstance(heap, list):
        raise TypeError("heap must be an list object")
    if len(heap) == 0:
        return "Nothing to print: heap is empty."

    output = io.StringIO()
    last_row = -1
    h_space = 3.0  # float
    v_space = 2  # int

    for i, heap_node in enumerate(heap):
        if i != 0:
            row = int(math.floor(math.log(i + 1, 2)))
        else:
            row = 0

        if row != last_row:
            output.write("\n" * v_space)

        columns = 2 ** row
        column_width = int(math.floor((total_width * h_space) / columns))
        output.write(str(heap_node).center(column_width, fill))
        last_row = row

    s = output.getvalue() + "\n"
    line_length = total_width + 15  # int
    s += ('-' * line_length + "\n")
    return s
