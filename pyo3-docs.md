## pyo30.23.3

  * All Items

### Sections

  * PyO3’s object types
    * The `Python<'py>` object, and the `'py` lifetime
    * Python object smart pointers
    * PyErr
  * Feature flags
    * Default feature flags
    * Optional feature flags
    * Unstable features
    * `rustc` environment flags
  * Minimum supported Rust and Python versions
  * Example: Building a native Python module
  * Example: Using Python from Rust
  * Other Examples

### Crate Items

  * Re-exports
  * Modules
  * Macros
  * Structs
  * Traits
  * Functions
  * Type Aliases
  * Attribute Macros
  * Derive Macros

# Crate pyo3

Source

Expand description

Rust bindings to the Python interpreter.

PyO3 can be used to write native Python modules or run Python code and modules from Rust.

See the guide for a detailed introduction.

## §PyO3’s object types

PyO3 has several core types that you should familiarize yourself with:

### §The `Python<'py>` object, and the `'py` lifetime

Holding the global interpreter lock (GIL) is modeled with the `Python<'py>` token. Many Python APIs require that the GIL is held, and PyO3 uses this token as proof that these APIs can be called safely. It can be explicitly acquired and is also implicitly acquired by PyO3 as it wraps Rust functions and structs into Python functions and objects.

The `Python<'py>` token’s lifetime `'py` is common to many PyO3 APIs:

  * Types that also have the `'py` lifetime, such as the `Bound<'py, T>` smart pointer, are bound to the Python GIL and rely on this to offer their functionality. These types often have a `.py()` method to get the associated `Python<'py>` token.
  * Functions which depend on the `'py` lifetime, such as `PyList::new`, require a `Python<'py>` token as an input. Sometimes the token is passed implicitly by taking a `Bound<'py, T>` or other type which is bound to the `'py` lifetime.
  * Traits which depend on the `'py` lifetime, such as `FromPyObject<'py>`, usually have inputs or outputs which depend on the lifetime. Adding the lifetime to the trait allows these inputs and outputs to express their binding to the GIL in the Rust type system.

### §Python object smart pointers

PyO3 has two core smart pointers to refer to Python objects, `Py<T>` and its GIL-bound form `Bound<'py, T>` which carries the `'py` lifetime. (There is also `Borrowed<'a, 'py, T>`, but it is used much more rarely).

The type parameter `T` in these smart pointers can be filled by:

  * `PyAny`, e.g. `Py<PyAny>` or `Bound<'py, PyAny>`, where the Python object type is not known. `Py<PyAny>` is so common it has a type alias `PyObject`.
  * Concrete Python types like `PyList` or `PyTuple`.
  * Rust types which are exposed to Python using the `#[pyclass]` macro.

See the guide for an explanation of the different Python object types.

### §PyErr

The vast majority of operations in this library will return `PyResult<...>`. This is an alias for the type `Result<..., PyErr>`.

A `PyErr` represents a Python exception. A `PyErr` returned to Python code will be raised as a Python exception. Errors from `PyO3` itself are also exposed as Python exceptions.

## §Feature flags

PyO3 uses feature flags to enable you to opt-in to additional functionality. For a detailed description, see the Features chapter of the guide.

### §Default feature flags

The following features are turned on by default:

  * `macros`: Enables various macros, including all the attribute macros.

### §Optional feature flags

The following features customize PyO3’s behavior:

  * `abi3`: Restricts PyO3’s API to a subset of the full Python API which is guaranteed by PEP 384 to be forward-compatible with future Python versions.
  * `auto-initialize`: Changes `Python::with_gil` to automatically initialize the Python interpreter if needed.
  * `extension-module`: This will tell the linker to keep the Python symbols unresolved, so that your module can also be used with statically linked Python interpreters. Use this feature when building an extension module.
  * `multiple-pymethods`: Enables the use of multiple `#[pymethods]` blocks per `#[pyclass]`. This adds a dependency on the inventory crate, which is not supported on all platforms.

The following features enable interactions with other crates in the Rust ecosystem:

  * `anyhow`: Enables a conversion from anyhow’s `Error` type to `PyErr`.
  * `chrono`: Enables a conversion from chrono’s structures to the equivalent Python ones.
  * `chrono-tz`: Enables a conversion from chrono-tz’s `Tz` enum. Requires Python 3.9+.
  * `either`: Enables conversions between Python objects and either’s `Either` type.
  * `eyre`: Enables a conversion from eyre’s `Report` type to `PyErr`.
  * `hashbrown`: Enables conversions between Python objects and hashbrown’s `HashMap` and `HashSet` types.
  * `indexmap`: Enables conversions between Python dictionary and indexmap’s `IndexMap`.
  * `num-bigint`: Enables conversions between Python objects and num-bigint’s `BigInt` and `BigUint` types.
  * `num-complex`: Enables conversions between Python objects and num-complex’s `Complex` type.
  * `num-rational`: Enables conversions between Python’s fractions.Fraction and num-rational’s types
  * `rust_decimal`: Enables conversions between Python’s decimal.Decimal and rust_decimal’s `Decimal` type.
  * `serde`: Allows implementing serde’s `Serialize` and `Deserialize` traits for `Py``<T>` for all `T` that implement `Serialize` and `Deserialize`.
  * `smallvec`: Enables conversions between Python list and smallvec’s `SmallVec`.

### §Unstable features

  * `nightly`: Uses `#![feature(auto_traits, negative_impls)]` to define `Ungil` as an auto trait.

### §`rustc` environment flags

  * `Py_3_7`, `Py_3_8`, `Py_3_9`, `Py_3_10`, `Py_3_11`, `Py_3_12`, `Py_3_13`: Marks code that is only enabled when compiling for a given minimum Python version.
  * `Py_LIMITED_API`: Marks code enabled when the `abi3` feature flag is enabled.
  * `Py_GIL_DISABLED`: Marks code that runs only in the free-threaded build of CPython.
  * `PyPy` \- Marks code enabled when compiling for PyPy.
  * `GraalPy` \- Marks code enabled when compiling for GraalPy.

Additionally, you can query for the values `Py_DEBUG`, `Py_REF_DEBUG`, `Py_TRACE_REFS`, and `COUNT_ALLOCS` from `py_sys_config` to query for the corresponding C build-time defines. For example, to conditionally define debug code using `Py_DEBUG`, you could do:

ⓘ

```
#[cfg(py_sys_config = "Py_DEBUG")]
println!("only runs if python was compiled with Py_DEBUG")
```

To use these attributes, add `pyo3-build-config` as a build dependency in your `Cargo.toml` and call `pyo3_build_config::use_pyo3_cfgs()` in a `build.rs` file.

## §Minimum supported Rust and Python versions

Requires Rust 1.63 or greater.

PyO3 supports the following Python distributions:

  * CPython 3.7 or greater
  * PyPy 7.3 (Python 3.9+)
  * GraalPy 24.0 or greater (Python 3.10+)

## §Example: Building a native Python module

PyO3 can be used to generate a native Python module. The easiest way to try this out for the first time is to use `maturin`. `maturin` is a tool for building and publishing Rust-based Python packages with minimal configuration. The following steps set up some files for an example Python module, install `maturin`, and then show how to build and import the Python module.

First, create a new folder (let’s call it `string_sum`) containing the following two files:

**`Cargo.toml`**

```
[package]
name = "string-sum"
version = "0.1.0"
edition = "2021"

[lib]
name = "string_sum"
# "cdylib" is necessary to produce a shared library for Python to import from.
#
# Downstream Rust code (including code in `bin/`, `examples/`, and `tests/`) will not be able
# to `use string_sum;` unless the "rlib" or "lib" crate type is also included, e.g.:
# crate-type = ["cdylib", "rlib"]
crate-type = ["cdylib"]

[dependencies.pyo3]
version = "0.23.3"
features = ["extension-module"]
```

**`src/lib.rs`**

```
use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn string_sum(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;

    Ok(())
}
```

With those two files in place, now `maturin` needs to be installed. This can be done using Python’s package manager `pip`. First, load up a new Python `virtualenv`, and install `maturin` into it:

```
$ cd string_sum
$ python -m venv .env
$ source .env/bin/activate
$ pip install maturin
```

Now build and execute the module:

```
$ maturin develop
# lots of progress output as maturin runs the compilation...
$ python
>>> import string_sum
>>> string_sum.sum_as_string(5, 20)
'25'
```

As well as with `maturin`, it is possible to build using setuptools-rust or manually. Both offer more flexibility than `maturin` but require further configuration.

## §Example: Using Python from Rust

To embed Python into a Rust binary, you need to ensure that your Python installation contains a shared library. The following steps demonstrate how to ensure this (for Ubuntu), and then give some example code which runs an embedded Python interpreter.

To install the Python shared library on Ubuntu:

```
sudo apt install python3-dev
```

Start a new project with `cargo new` and add `pyo3` to the `Cargo.toml` like this:

```
[dependencies.pyo3]
version = "0.23.3"
# this is necessary to automatically initialize the Python interpreter
features = ["auto-initialize"]
```

Example program displaying the value of `sys.version` and the current user name:

```
use pyo3::prelude::*;
use pyo3::types::IntoPyDict;
use pyo3::ffi::c_str;

fn main() -> PyResult<()> {
    Python::with_gil(|py| {
        let sys = py.import("sys")?;
        let version: String = sys.getattr("version")?.extract()?;

        let locals = [("os", py.import("os")?)].into_py_dict(py)?;
        let code = c_str!("os.getenv('USER') or os.getenv('USERNAME') or 'Unknown'");
        let user: String = py.eval(code, None, Some(&locals))?.extract()?;

        println!("Hello {}, I'm Python {}", user, version);
        Ok(())
    })
}
```

The guide has a section with lots of examples about this topic.

## §Other Examples

The PyO3 README contains quick-start examples for both using Rust from Python and Python from Rust.

The PyO3 repository’s examples subdirectory contains some basic packages to demonstrate usage of PyO3.

There are many projects using PyO3 - see a list of some at https://github.com/PyO3/pyo3#examples.

## Re-exports§

`pub use crate::conversion::AsPyPointer;`

`pub use crate::conversion::FromPyObject;`

`pub use crate::conversion::IntoPyObject;`

`pub use crate::conversion::IntoPyObjectExt;`

`pub use crate::conversion::IntoPy;`Deprecated

`pub use crate::conversion::ToPyObject;`Deprecated

`pub use crate::marker::Python;`

`pub use crate::pycell::PyRef;`

`pub use crate::pycell::PyRefMut;`

`pub use crate::pyclass::PyClass;`

`pub use crate::pyclass_init::PyClassInitializer;`

`pub use crate::type_object::PyTypeCheck;`

`pub use crate::type_object::PyTypeInfo;`

`pub use crate::types::PyAny;`

`pub use crate::class::*;`

## Modules§

anyhow

    A conversion from anyhow’s `Error` type to `PyErr`.
buffer

    `PyBuffer` implementation
call

    Defines how Python calls are dispatched, see `PyCallArgs`.for more information.
chrono

    Conversions to and from chrono’s `Duration`, `NaiveDate`, `NaiveTime`, `DateTime<Tz>`, `FixedOffset`, and `Utc`.
class

    Old module which contained some implementation details of the `#[pyproto]` module.
conversion

    Defines conversions between Rust and Python types.
coroutine

    Python coroutine implementation, used notably when wrapping `async fn` with `#[pyfunction]`/`#[pymethods]`.
either

    Conversion to/from either’s `Either` type to a union of two Python types.
exceptions

    Exception and warning types defined by Python.
eyre

    A conversion from eyre’s `Report` type to `PyErr`.
ffi

    Raw FFI declarations for Python’s C API.
hashbrown

    Conversions to and from hashbrown’s `HashMap` and `HashSet`.
indexmap

    Conversions to and from indexmap’s `IndexMap`.
inspect

    Runtime inspection of objects exposed to Python.
jiff

    Conversions to and from jiff’s `Span`, `SignedDuration`, `TimeZone`, `Offset`, `Date`, `Time`, `DateTime`, `Zoned`, and `Timestamp`.
marker

    Fundamental properties of objects tied to the Python interpreter.
marshal

    Support for the Python `marshal` format.
num_bigint

    Conversions to and from num-bigint’s `BigInt` and `BigUint` types.
num_complex

    Conversions to and from num-complex’ `Complex``<``f32``>` and `Complex``<``f64``>`.
num_rational

    Conversions to and from num-rational types.
panic

    Helper to convert Rust panics to Python exceptions.
prelude

    PyO3’s prelude.
pybacked

    Contains types for working with Python objects that own the underlying data.
pycell

    PyO3’s interior mutability primitive.
pyclass

    `PyClass` and related traits.
pyclass_init

    Contains initialization utilities for `#[pyclass]`.
rust_decimal

    Conversions to and from rust_decimal’s [`Decimal`] type.
serde

    Enables (de)serialization of `Py``<T>` objects via serde.
smallvec

    Conversions to and from smallvec.
sync

    Synchronization mechanisms based on the Python GIL.
type_object

    Python type object information
types

    Various types defined by the Python interpreter such as `int`, `str` and `tuple`.
uuid

    Conversions to and from uuid’s `Uuid` type.

## Macros§

append_to_inittab

    Add the module to the initialization table in order to make embedded Python code to use it. Module name is the argument.
create_exception

    Defines a new exception type.
import_exception

    Defines a Rust type for an exception defined in Python code.
import_exception_bound

    Variant of `import_exception` that does not emit code needed to use the imported exception type as a GIL Ref.
intern

    Interns `text` as a Python string and stores a reference to it in static storage.
py_run

    A convenient macro to execute a Python code snippet, with some local variables set.
wrap_pyfunction

    Wraps a Rust function annotated with `#[pyfunction]`.
wrap_pyfunction_boundDeprecated

    Wraps a Rust function annotated with `#[pyfunction]`.
wrap_pymodule

    Returns a function that takes a `Python` instance and returns a Python module.

## Structs§

Borrowed

    A borrowed equivalent to `Bound`.
Bound

    A GIL-attached equivalent to `Py<T>`.
DowncastError

    Error that indicates a failure to convert a PyAny to a more specific Python type.
DowncastIntoError

    Error that indicates a failure to convert a PyAny to a more specific Python type.
Py

    A GIL-independent reference to an object allocated on the Python heap.
PyErr

    Represents a Python exception.
PythonVersionInfo

    Represents the major, minor, and patch (if any) versions of this interpreter.

## Traits§

BoundObject

    Owned or borrowed gil-bound Python smart pointer
PyErrArguments

    Helper conversion trait that allows to use custom arguments for lazy exception construction.
ToPyErr

    Python exceptions that can be converted to `PyErr`.

## Functions§

prepare_freethreaded_python

    Prepares the use of Python in a free-threaded context.
with_embedded_python_interpreter⚠

    Executes the provided closure with an embedded Python interpreter.

## Type Aliases§

PyObject

    A commonly-used alias for `Py<PyAny>`.
PyResult

    Represents the result of a Python call.

## Attribute Macros§

pyclass

    A proc macro used to expose Rust structs and fieldless enums as Python objects.
pyfunction

    A proc macro used to expose Rust functions to Python.
pymethods

    A proc macro used to expose methods to Python.
pymodule

    A proc macro used to implement Python modules.

## Derive Macros§

FromPyObject

IntoPyObject

IntoPyObjectRef