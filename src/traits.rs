use anyhow::{Error, Result};
use foldhash::fast::RandomState;
use indexmap::IndexMap;
use reqwest::header::{HeaderMap, HeaderName, HeaderValue};

type IndexMapSSR = IndexMap<String, String, RandomState>;

pub trait HeadersTraits {
    fn to_indexmap(&self) -> IndexMapSSR;
    fn to_headermap(&self) -> HeaderMap;
    fn insert_key_value(&mut self, key: String, value: String) -> Result<(), Error>;
}

impl HeadersTraits for IndexMapSSR {
    fn to_indexmap(&self) -> IndexMapSSR {
        self.clone()
    }
    fn to_headermap(&self) -> HeaderMap {
        let mut header_map = HeaderMap::with_capacity(self.len());
        for (k, v) in self {
            // Skip invalid headers with a warning instead of panicking
            match (
                HeaderName::from_bytes(k.as_bytes()),
                HeaderValue::from_bytes(v.as_bytes()),
            ) {
                (Ok(name), Ok(value)) => {
                    header_map.insert(name, value);
                }
                (Err(e), _) => {
                    tracing::warn!("Skipping invalid header name '{}': {}", k, e);
                }
                (_, Err(e)) => {
                    tracing::warn!("Skipping invalid header value for '{}': {}", k, e);
                }
            }
        }
        header_map
    }

    fn insert_key_value(&mut self, key: String, value: String) -> Result<(), Error> {
        self.insert(key.to_string(), value.to_string());
        Ok(())
    }
}

impl HeadersTraits for HeaderMap {
    fn to_indexmap(&self) -> IndexMapSSR {
        let mut index_map =
            IndexMapSSR::with_capacity_and_hasher(self.len(), RandomState::default());
        for (key, value) in self {
            // Store the original header name (preserving case)
            let header_name = key.as_str().to_string();
            // Skip invalid header values with a warning instead of panicking
            match value.to_str() {
                Ok(v) => {
                    index_map.insert(header_name, v.to_string());
                }
                Err(e) => {
                    tracing::warn!("Skipping header '{}' with invalid value: {}", key, e);
                }
            }
        }
        index_map
    }

    fn to_headermap(&self) -> HeaderMap {
        self.clone()
    }

    fn insert_key_value(&mut self, key: String, value: String) -> Result<(), Error> {
        let header_name = HeaderName::from_bytes(key.as_bytes())
            .map_err(|e| Error::msg(format!("Invalid header name '{}': {}", key, e)))?;
        let header_value = HeaderValue::from_bytes(value.as_bytes())
            .map_err(|e| Error::msg(format!("Invalid header value for '{}': {}", key, e)))?;
        self.insert(header_name, header_value);
        Ok(())
    }
}

pub trait CookiesTraits {
    fn to_string(&self) -> String;
}

impl CookiesTraits for IndexMapSSR {
    fn to_string(&self) -> String {
        let mut result = String::with_capacity(self.len() * 40);
        for (k, v) in self {
            if !result.is_empty() {
                result.push_str("; ");
            }
            result.push_str(k);
            result.push('=');
            result.push_str(v);
        }
        result
    }
}
