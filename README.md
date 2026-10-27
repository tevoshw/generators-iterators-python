# Iterators and Generators in Python

A summary of what we covered, from the basics to classes and PyTorch.

---

## 1. Iterable vs Iterator

| | Iterable | Iterator |
|---|---|---|
| Has `__iter__` | yes | yes |
| Has `__next__` | no | **yes** |
| Remembers current position | no | **yes** |
| Examples | `list`, `str`, `dict`, `tuple` | the return value of `iter(my_list)` |

- **Iterable**: something that can be traversed (the book).
- **Iterator**: the object that does the traversing and remembers where it stopped (the bookmark).

```python
numbers = [10, 20, 30]
it = iter(numbers)    # creates a separate iterator

print(next(it))       # 10
print(next(it))       # 20
print(next(it))       # 30
next(it)              # StopIteration
```

Key points:

- The original list is **not changed**. The iterator is a separate object.
- `next([1, 2, 3])` fails (a list is not an iterator). `next(iter([1, 2, 3]))` works.
- Once exhausted, an iterator **does not go back to the start**. You need to create a new one with `iter()`.
- Everything in Python is already an object. The iterator doesn't "turn something into an object"; it is an **extra** object that has `__next__`.

---

## 2. The special methods

| You write | Python calls |
|---|---|
| `iter(obj)` | `obj.__iter__()` |
| `next(obj)` | `obj.__next__()` |
| `for x in obj` | `iter(obj)` once, then `next()` repeatedly |

### `__next__`: the logic

Three responsibilities:

```python
def __next__(self):
    if self.current >= self.limit:   # 1) finished? signal it
        raise StopIteration
    self.current += 1                # 2) update the state
    return self.current              # 3) return the value
```

### `__iter__`: "which object traverses you?"

It must return **an iterator** (an object with `__next__`).

- In an iterator class: `return self` (the object already has `__next__`).
- In a list: it returns a new object (`list_iterator`).

```python
iter(my_list) is my_list   # False -> returned a different object
iter(c) is c               # True  -> return self
```

> `return self` does **not** give anything iterator powers. The power comes from having `__next__`.
> If it's missing, you get `TypeError: iter() returned non-iterator`.

---

## 3. Iterator class (writing everything by hand)

```python
class Evens:
    def __init__(self, limit):
        self.limit = limit
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.current += 2
        if self.current > self.limit:
            raise StopIteration
        return self.current


e = Evens(6)
print(next(e))   # 2
print(next(e))   # 4
print(next(e))   # 6
next(e)          # StopIteration
```

- `__init__` runs when the object is **created**: `Evens(6)`.
- `self.current` persists between calls, which is what makes the iterator "remember where it stopped".
- The object is already the iterator, so `next(e)` works directly, without `iter()`.

### Iterable class (only `__iter__`, returns another iterator)

```python
class Team:
    def __init__(self, players):
        self.players = players

    def __iter__(self):
        return iter(self.players)

t = Team(["Ana", "Bia", "Caio"])

for p in t: print(p)   # works
for p in t: print(p)   # works again
next(t)                # TypeError (t is iterable, not an iterator)
```

| Class has | So it is | `next(obj)` | `for x in obj` |
|---|---|---|---|
| `__iter__` + `__next__` | iterator | works | works |
| only `__iter__` | iterable | no | works |

---

## 4. Functions and iterators

- **Regular function** (`return`): does not become an iterator. It runs, returns, and forgets everything.
- **Function with `yield`**: when **called**, it returns an object that **is already an iterator** (the generator).

---

## 5. Generators and `yield`

### Three different terms

| Term | What it is |
|---|---|
| `yield` | Keyword: returns a value and **pauses** |
| Generator function | The function that contains `yield` (the "recipe") |
| Generator (object) | What you get when you **call** the generator function |

```python
def evens(limit):           # generator function
    current = 2
    while current <= limit:
        yield current       # returns and pauses
        current += 2

g = evens(6)                # g is the generator (object)
print(next(g))              # 2
print(next(g))              # 4
print(next(g))              # 6
next(g)                     # StopIteration
```

### What `yield` does

1. Returns a value (like `return`).
2. **Pauses** the function, keeping local variables and the line where it stopped.

On the next `next()`, it continues from where it paused.

```python
def count():
    print("start")
    yield 1
    print("middle")
    yield 2
    print("end")

g = count()
next(g)   # prints "start", returns 1
next(g)   # prints "middle", returns 2
next(g)   # prints "end", StopIteration
```

| | `return` | `yield` |
|---|---|---|
| Returns a value | yes | yes |
| Ends the function | **yes** | no, only pauses |
| Keeps local variables | no | yes |

### What Python does for you

| Iterator class (you write it) | Generator (Python does it) |
|---|---|
| `__next__` returns the next value | `yield value` |
| `self.current` stores the position | local variable preserved during the pause |
| `raise StopIteration` | the function finishing |
| `__iter__` with `return self` | created automatically |

The generator **really has** `__next__` and `__iter__`:

```python
hasattr(g, "__next__")   # True
iter(g) is g             # True
```

> You don't **write** `__next__`, but you still **use** `next()` (or `for`) to get the values.

---

## 6. Iterator vs Generator

**A generator is a kind of iterator.** Every generator is an iterator, but not every iterator is a generator (`list_iterator` and the `Evens` class with `__next__` are not generators).

| | Iterator (manual class) | Generator |
|---|---|---|
| How to create | Class with `__iter__` and `__next__` | Function with `yield` (or `(x for x in ...)`) |
| Who writes `__iter__`/`__next__` | You | Python |
| Where state is kept | You, in `self.current` | Python, in local variables |
| How the end is signaled | `raise StopIteration` | The function finishing |
| Amount of code | More | Less |

**When to use each**

- **Generator**: in most cases (shorter and more readable).
- **Iterator class**: when you need something extra, like `reset()`, `peek()`, several public attributes, or inheritance.

---

## 7. `yield` inside classes

### 7.1. `yield` in `__iter__` (the most common)

The class becomes **iterable** and works in a `for`, with no `__next__`:

```python
class Evens:
    def __init__(self, limit):
        self.limit = limit

    def __iter__(self):
        current = 2
        while current <= self.limit:   # logic lives in __iter__
            yield current
            current += 2

e = Evens(6)          # instantiate normally (only runs __init__)
print(list(e))        # [2, 4, 6]
print(list(e))        # [2, 4, 6]  (can be traversed again)
```

Why it works: with `yield`, `__iter__` becomes a generator function. Each `for` calls `iter(e)` and receives **a new generator**.

Details:

- **Instantiation** is always `Evens(6)`. `iter()` is not for instantiating, it's for **traversing**.
- `__iter__` only runs when you iterate (`for`, `iter()`, `list()`, `sum()`...).
- Calling `next(e)` directly fails, because `e` is iterable, not an iterator. Use `next(iter(e))`.
- You can only put logic in `__iter__` **if it has `yield`**. Without `yield`, it must return an iterator.

### 7.2. `yield` in regular methods

```python
class Team:
    def __init__(self, players):
        self.players = players

    def starters(self):
        for p in self.players[:2]:
            yield p

    def substitutes(self):
        for p in self.players[2:]:
            yield p

t = Team(["Ana", "Bia", "Caio", "Davi"])
print(list(t.starters()))       # ['Ana', 'Bia']
print(list(t.substitutes()))    # ['Caio', 'Davi']
```

### 7.3. `yield from` (delegating)

```python
def __iter__(self):
    yield from self.players
# equivalent to: for p in self.players: yield p
```

---

## 8. PyTorch: why don't I use `next()`?

The `for` loop already calls `iter()` and `next()` for you. This is true with or without `yield`.

```python
for batch in loader:    # 1) iter(loader)
    ...                 # 2) repeated next(), until StopIteration
```

`yield` only defines **how the data is produced**. The `DataLoader` + `for` take care of **consuming** it.

| Type | You write | Uses `yield`? |
|---|---|---|
| Map-style (`Dataset`) | `__getitem__` and `__len__` | No, uses `return` |
| Iterable-style (`IterableDataset`) | `__iter__` | **Yes** |

```python
from torch.utils.data import IterableDataset, DataLoader

class MyStream(IterableDataset):
    def __init__(self, data):
        self.data = data

    def __iter__(self):
        for x in self.data:
            yield x

loader = DataLoader(MyStream(range(10)), batch_size=4)

for batch in loader:
    print(batch)

# To inspect just one batch (shape debugging):
first = next(iter(loader))
```

Example of a class that yields data in batches (same idea as a `DataLoader`):

```python
class Batches:
    def __init__(self, data, size):
        self.data = data
        self.size = size

    def __iter__(self):
        for i in range(0, len(self.data), self.size):
            yield self.data[i:i + self.size]
```

---

## 9. The full `for` flow

```python
for x in obj:
    ...
```

is equivalent to:

```python
it = iter(obj)            # calls obj.__iter__()
while True:
    try:
        x = next(it)      # calls it.__next__()
    except StopIteration:
        break
    ...
```

If `obj.__iter__` has `yield`, then `it` is a generator, and its `__next__` was created by Python.

---

## 10. Final summary

| Piece | Role |
|---|---|
| `iter(obj)` | Calls `obj.__iter__()` |
| `next(it)` | Calls `it.__next__()` |
| `__iter__` | Returns **the iterator** (`self`, `iter(list)`, or a generator if it has `yield`) |
| `__next__` | Logic for the next value and `StopIteration` at the end |
| `yield` | Makes Python create `__iter__` and `__next__` from a function |
| `for` | Calls `iter()` once and `next()` until it's done |

**Key sentences**

> An iterator is an object with `__next__` that returns one value at a time and remembers where it stopped.

> A generator is a kind of iterator created with `yield`, where Python writes `__next__` for me.

> `yield` plays the role of `__next__` in my code, but the real `__next__` exists on the generator object.

## Gotchas

- Iterators and generators are **single-use**: once exhausted, you need to create a new one.
- Generators don't support `len()` or indexing (`g[0]`).
- `return self` in `__iter__` only works if the class has `__next__`.
- A class with `yield` in `__iter__` is **iterable**, not an iterator: calling `next(obj)` directly fails.

## Practice exercises

1. An iterator class `Fibonacci` with `__iter__` + `__next__`.
2. The same `Fibonacci` with `yield` in `__iter__`.
3. A generator `batches(data, size)` that yields batches from a list.