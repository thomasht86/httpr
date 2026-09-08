//! Query-string and form-body parameters.
//!
//! Python callers hand `params` and `data` over as a mapping (or a sequence of
//! `(key, value)` pairs) whose values may be `str`, `int`, `float`, `bool`,
//! `None`, or a `list`/`tuple` of those. They are normalised here into ordered
//! `(key, value)` string pairs following httpx's rules, so that reqwest can
//! serialise them with repeated keys for multi-value entries:
//!
//! * `True`/`False` become `"true"`/`"false"`
//! * `None` becomes the empty string
//! * a `list` or `tuple` repeats the key once per element
//! * everything else goes through `str()`
//!
//! (issue #87). Client-level params are merged with per-request params here
//! too (issue #82).

use pyo3::exceptions::PyTypeError;
use pyo3::prelude::*;
use pyo3::types::{PyBool, PyDict, PyList, PyString, PyTuple};

/// Ordered `(key, value)` pairs, possibly with repeated keys.
pub type Pairs = Vec<(String, String)>;

/// httpx's `primitive_value_to_str`.
fn primitive_to_string(value: &Bound<'_, PyAny>) -> PyResult<String> {
    if value.is_none() {
        return Ok(String::new());
    }
    if let Ok(b) = value.cast::<PyBool>() {
        return Ok(if b.is_true() { "true" } else { "false" }.to_owned());
    }
    if let Ok(s) = value.cast::<PyString>() {
        return Ok(s.to_str()?.to_owned());
    }
    Ok(value.str()?.to_str()?.to_owned())
}

fn push_entry(out: &mut Pairs, key: &Bound<'_, PyAny>, value: &Bound<'_, PyAny>) -> PyResult<()> {
    let key = primitive_to_string(key)?;
    if value.is_instance_of::<PyList>() || value.is_instance_of::<PyTuple>() {
        for item in value.try_iter()? {
            out.push((key.clone(), primitive_to_string(&item?)?));
        }
    } else {
        out.push((key, primitive_to_string(value)?));
    }
    Ok(())
}

/// Normalises a Python mapping or sequence of `(key, value)` pairs into
/// string pairs. `what` names the argument in the `TypeError` raised for any
/// other shape.
pub fn normalize_params(obj: &Bound<'_, PyAny>, what: &str) -> PyResult<Pairs> {
    let type_error = || {
        PyTypeError::new_err(format!(
            "{what} must be a mapping or a sequence of (key, value) pairs, got {}",
            obj.get_type()
        ))
    };

    if let Ok(dict) = obj.cast::<PyDict>() {
        let mut out = Vec::with_capacity(dict.len());
        for (key, value) in dict.iter() {
            push_entry(&mut out, &key, &value)?;
        }
        return Ok(out);
    }

    // Any other mapping (MappingProxy, httpx.QueryParams, ...) via `items()`;
    // a `str`/`bytes` is iterable but never a sequence of pairs.
    if obj.is_instance_of::<PyString>() || obj.is_instance_of::<pyo3::types::PyBytes>() {
        return Err(type_error());
    }
    let items = if obj.hasattr("items")? {
        obj.call_method0("items")?
    } else {
        obj.clone()
    };
    let mut out = Vec::new();
    for item in items.try_iter().map_err(|_| type_error())? {
        let item = item?;
        let (key, value): (Bound<'_, PyAny>, Bound<'_, PyAny>) =
            item.extract().map_err(|_| type_error())?;
        push_entry(&mut out, &key, &value)?;
    }
    Ok(out)
}

/// Client-level pairs followed by the request's own. A key the request supplies
/// replaces every client value for that key, as in httpx; keys only the client
/// has are kept.
pub fn merge_params(client: &[(String, String)], request: Pairs) -> Pairs {
    if client.is_empty() {
        return request;
    }
    let mut out: Pairs = client
        .iter()
        .filter(|(key, _)| !request.iter().any(|(rk, _)| rk == key))
        .cloned()
        .collect();
    out.extend(request);
    out
}

/// The Python view of stored pairs: a dict whose values are a `str`, or a
/// `list[str]` for a key that appears more than once. Feeding it back to the
/// setter reproduces the same pairs.
pub fn params_to_py<'py>(
    py: Python<'py>,
    pairs: &[(String, String)],
) -> PyResult<Bound<'py, PyDict>> {
    let dict = PyDict::new(py);
    for (key, value) in pairs {
        match dict.get_item(key)? {
            None => dict.set_item(key, value)?,
            Some(existing) => {
                if let Ok(list) = existing.cast::<PyList>() {
                    list.append(value)?;
                } else {
                    let list = PyList::new(py, [existing])?;
                    list.append(value)?;
                    dict.set_item(key, list)?;
                }
            }
        }
    }
    Ok(dict)
}
