use std::cmp::min;

use reqwest::Certificate;
use tracing;

use std::{env, fs};

use anyhow::{Context, Result};

/// Load CA certificates from a file specified by the environment variable `HTTPR_CA_BUNDLE`.
pub fn load_ca_certs() -> Result<Vec<Certificate>> {
    let ca_bundle_path = env::var("HTTPR_CA_BUNDLE").ok();

    match ca_bundle_path {
        Some(path) => {
            tracing::info!("Loading CA certificates from {}", path);
            let ca_certs = read_pem_certificates(&path)
                .with_context(|| format!("Failed to read CA certificates from {}", path))?;
            Ok(ca_certs)
        }
        None => {
            tracing::info!("HTTPR_CA_BUNDLE environment variable not set. Skipping loading CA certificates.");
            Ok(Vec::new())
        }
    }
}

fn read_pem_certificates(path: &str) -> Result<Vec<Certificate>> {
    let cert_bytes = fs::read(path).context("Failed to read certificate file")?;
    let mut certificates = vec![];
    let mut cursor = std::io::Cursor::new(cert_bytes);
    while let Ok(Some(cert)) = rustls_pemfile::read_one(&mut cursor) {
        match cert {
            rustls_pemfile::Item::X509Certificate(cert) => {
                let certificate = Certificate::from_der(&cert)?;
                certificates.push(certificate);
            }
            _ => {
                tracing::warn!("Skipping non-certificate item");
            }
        }
    }
    Ok(certificates)
}

/// Get encoding from the "Content-Type" header using CaseInsensitiveHeaderMap
pub fn get_encoding_from_case_insensitive_headers(
    headers: &crate::response::CaseInsensitiveHeaderMap
) -> Option<String> {
    if headers.contains_key("content-type") {
        let content_type = headers.get_value("content-type")?;
        
        // Parse the Content-Type header to separate the media type and parameters
        let mut parts = content_type.split(';');
        let media_type = parts.next().unwrap_or("").trim();
        let params = parts.next().unwrap_or("").trim();

        // Check for specific conditions and return the appropriate encoding
        if let Some(param) = params.to_ascii_lowercase().strip_prefix("charset=") {
            Some(param.trim_matches('"').to_ascii_lowercase())
        } else if media_type == "application/json" {
            Some("utf-8".to_string())
        } else {
            None
        }
    } else {
        None
    }
}

/// Get encoding from the `<meta charset="...">` tag within the first 2048 bytes of HTML content.
pub fn get_encoding_from_content(raw_bytes: &[u8]) -> Option<String> {
    let start_sequence: &[u8] = b"charset=";
    let max_index = min(2048, raw_bytes.len());

    if let Some(start_index) = raw_bytes[..max_index]
        .windows(start_sequence.len())
        .position(|window| window == start_sequence)
    {
        let remaining_bytes = &raw_bytes[start_index + start_sequence.len()..max_index];
        if let Some(end_index) = remaining_bytes
            .iter()
            .enumerate()
            .position(|(i, &byte)| matches!(byte, b' ' | b'"' | b'>') && i > 0)
        {
            let charset_slice = &remaining_bytes[..end_index];
            let charset = String::from_utf8_lossy(charset_slice)
                .trim_matches('"')
                .to_ascii_lowercase();
            return Some(charset);
        }
    }
    None
}

#[cfg(test)]
mod load_ca_certs_tests {
    use super::*;
    use std::env;
    use std::fs;
    use std::path::Path;

    #[test]
    fn test_load_ca_certs_with_env_var() {
        // Create a temporary file with a CA certificate
        let ca_cert_path = Path::new("test_ca_cert.pem");
        let ca_cert = "-----BEGIN CERTIFICATE-----
MIIDdTCCAl2gAwIBAgIVAMIIujU9wQIBADANBgkqhkiG9w0BAQUFADBGMQswCQYD
VQQGEwJVUzETMBEGA1UECAwKQ2FsaWZvcm5pYTEWMBQGA1UEBwwNTW91bnRhaW4g
Q29sbGVjdGlvbjEgMB4GA1UECgwXUG9zdGdyZXMgQ29uc3VsdGF0aW9uczEhMB8G
A1UECwwYUG9zdGdyZXMgQ29uc3VsdGF0aW9uczEhMB8GA1UEAwwYUG9zdGdyZXMg
Q29uc3VsdGF0aW9uczEiMCAGCSqGSIb3DQEJARYTcGVyc29uYWwtZW1haWwuY29t
MIIDdTCCAl2gAwIBAgIVAMIIujU9wQIBADANBgkqhkiG9w0BAQUFADBGMQswCQYD
VQQGEwJVUzETMBEGA1UECAwKQ2FsaWZvcm5pYTEWMBQGA1UEBwwNTW91bnRhaW4g
Q29sbGVjdGlvbjEgMB4GA1UECgwXUG9zdGdyZXMgQ29uc3VsdGF0aW9uczEhMB8G
A1UECwwYUG9zdGdyZXMgQ29uc3VsdGF0aW9uczEhMB8GA1UEAwwYUG9zdGdyZXMg
Q29uc3VsdGF0aW9uczEiMCAGCSqGSIb3DQEJARYTcGVyc29uYWwtZW1haWwuY29t
-----END CERTIFICATE-----";
        fs::write(ca_cert_path, ca_cert).unwrap();

        // Set the environment variable
        env::set_var("HTTPR_CA_BUNDLE", ca_cert_path);

        // Call the function
        let result = load_ca_certs();

        // Check the result
        assert!(result.is_ok());

        // Clean up
        fs::remove_file(ca_cert_path).unwrap();
    }

    #[test]
    fn test_load_ca_certs_without_env_var() {
        // Call the function
        let result = load_ca_certs();

        // Check the result
        assert!(result.is_ok());
    }
}

#[cfg(test)]
mod utils_tests {
    use super::*;
    use crate::response::CaseInsensitiveHeaderMap;

    #[test]
    fn test_get_encoding_from_case_insensitive_headers() {
        // Test case: Content-Type header with charset specified
        let mut headers = CaseInsensitiveHeaderMap::create();
        headers.insert(
            String::from("Content-Type"),
            String::from("text/html;charset=UTF-8"),
        );
        assert_eq!(
            get_encoding_from_case_insensitive_headers(&headers),
            Some("utf-8".to_string())
        );

        // Test case: Content-Type header without charset specified
        headers = CaseInsensitiveHeaderMap::create();
        headers.insert(String::from("Content-Type"), String::from("text/plain"));
        assert_eq!(get_encoding_from_case_insensitive_headers(&headers), None);

        // Test case: Missing Content-Type header
        let headers = CaseInsensitiveHeaderMap::create();
        assert_eq!(get_encoding_from_case_insensitive_headers(&headers), None);

        // Test case: Content-Type header with application/json
        let mut headers = CaseInsensitiveHeaderMap::create();
        headers.insert(
            String::from("Content-Type"),
            String::from("application/json"),
        );
        assert_eq!(
            get_encoding_from_case_insensitive_headers(&headers),
            Some("utf-8".to_string())
        );
    }

    #[test]
    fn test_get_encoding_from_content_present_charset() {
        let raw_html = b"<html><head><meta charset=windows1252\"></head></html>";
        assert_eq!(
            get_encoding_from_content(raw_html),
            Some("windows1252".to_string())
        );
    }

    #[test]
    fn test_get_encoding_from_content_present_charset2() {
        let raw_html = b"<html><head><meta charset=\"windows1251\"></head></html>";
        assert_eq!(
            get_encoding_from_content(raw_html),
            Some("windows1251".to_string())
        );
    }

    #[test]
    fn test_get_encoding_from_content_present_charset3() {
        let raw_html =
            b"<html><head><meta charset=\"UTF-8\" src=\"https://www.gstatic.com/\" ></head></html>";
        assert_eq!(
            get_encoding_from_content(raw_html),
            Some("utf-8".to_string())
        );
    }

    #[test]
    fn test_get_encoding_from_content_missing_charset() {
        let raw_html = b"<html><head></head></html>";
        assert_eq!(get_encoding_from_content(raw_html), None);
    }
}
