# Python OOP Interview Q&A

## Question: What are the four pillars of OOP?
Encapsulation (bundling data and methods, restricting direct access via private/protected attributes), Abstraction (hiding implementation details, exposing only necessary interfaces), Inheritance (a class acquiring properties and methods of another class), and Polymorphism (same interface behaving differently based on the object — method overriding and duck typing).

## Question: How does Python implement encapsulation since it doesn't have true private members?
Python uses naming conventions rather than strict access control. A single underscore prefix (`_var`) signals "protected, internal use" by convention. A double underscore prefix (`__var`) triggers name mangling — Python renames it to `_ClassName__var` internally, making accidental access harder but not impossible. There's no compiler-enforced privacy like Java's `private` keyword.

## Question: What is the difference between `__init__` and `__new__`?
`__new__` is a static method that creates and returns a new instance of the class — it's called first and is responsible for allocating memory. `__init__` is an instance method that initializes the already-created object's attributes — it doesn't return anything. You override `__new__` rarely, typically for singletons or immutable types like subclassing `str` or `tuple`.

## Question: Explain Method Resolution Order (MRO) and the diamond problem.
MRO defines the order in which Python looks up methods in a hierarchy of multiple inheritance, using the C3 linearization algorithm. It ensures a consistent, predictable order and solves the "diamond problem" (where a class inherits from two classes that both inherit from a common base) by ensuring the base class is only processed once. You can inspect it via `ClassName.__mro__` or `ClassName.mro()`.

## Question: What is the difference between classmethod, staticmethod, and instance method?
An instance method takes `self` and can access/modify instance state. A `@classmethod` takes `cls` instead of `self`, operates on the class itself, and is often used for alternative constructors (e.g., `from_json`). A `@staticmethod` takes neither `self` nor `cls` — it behaves like a plain function namespaced inside the class, used for utility logic related to the class but not needing instance/class state.

## Question: What is duck typing in Python?
Duck typing means Python cares about what methods/behavior an object supports, not its explicit type — "if it walks like a duck and quacks like a duck, it's a duck." You can pass any object to a function as long as it implements the expected methods, without needing inheritance from a common interface. This is why Python supports polymorphism without requiring explicit interface declarations like in Java.

## Question: What is the difference between `is` and `==`?
`==` checks value equality (calls `__eq__`), comparing whether two objects have the same content. `is` checks identity equality — whether two references point to the exact same object in memory. For example, two separate lists with identical contents are `==` but not `is`.

## Question: Explain the concept of abstract base classes (ABC) in Python.
Python's `abc` module lets you define abstract base classes with `@abstractmethod` decorators. A class inheriting from `ABC` cannot be instantiated directly if it has unimplemented abstract methods — subclasses must override them. This enforces a contract/interface, similar to Java's abstract classes or interfaces.

## Question: What is multiple inheritance and how does Python handle conflicts?
Multiple inheritance lets a class inherit from more than one parent class. Python resolves attribute/method conflicts using MRO (C3 linearization) — it searches parent classes in a specific left-to-right, depth-first order (with the diamond problem correctly deduplicated), so the first matching method found in that order wins.

## Question: What are dunder (magic) methods? Give examples.
Dunder methods (double underscore) let you define how objects behave with built-in operations. Examples: `__init__` (constructor), `__str__` (string representation for `print()`), `__repr__` (developer-facing representation), `__len__` (enables `len(obj)`), `__eq__` (enables `==`), `__add__` (enables `+` operator overloading), `__iter__`/`__next__` (makes an object iterable).

## Question: What is the difference between composition and inheritance?
Inheritance models an "is-a" relationship — a subclass is a specialized version of its parent. Composition models a "has-a" relationship — a class contains instances of other classes as attributes to reuse their functionality. Composition is generally favored over inheritance for flexibility, since it avoids deep, fragile class hierarchies and allows behavior to be swapped at runtime.

## Question: What is a property decorator (`@property`) used for?
`@property` lets you define a method that can be accessed like an attribute (no parentheses needed), enabling getter/setter/deleter logic behind a clean attribute-style interface. It's used for computed attributes or to add validation when setting a value, while keeping the external API looking like simple attribute access rather than explicit `get_x()`/`set_x()` calls.

## Question: What is method overriding vs method overloading, and does Python support both?
Overriding means a subclass redefines a method already defined in its parent class — Python fully supports this natively. Overloading means having multiple methods with the same name but different parameters (common in Java/C++) — Python does NOT support true overloading; the last-defined method with that name wins. Python achieves similar flexibility using default arguments, `*args`/`**kwargs`, or the `functools.singledispatch` decorator.
