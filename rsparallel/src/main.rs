use futures::future::join_all;
use reqwest;
use reqwest::header::HeaderMap;
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::HashMap;
use std::error::Error;
use clap::Parser;
use tokio::time::{sleep, Duration};
use std::time::{Instant};
use log::{debug, info, error};

#[derive(Debug)]
struct RequestError {
    status: reqwest::StatusCode,
    message: String,
}

impl std::fmt::Display for RequestError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "HTTP {}: {}", self.status, self.message)
    }
}

impl Error for RequestError {}

impl From<reqwest::Error> for RequestError {
    fn from(err: reqwest::Error) -> Self {
        RequestError {
            status: err.status().unwrap_or_default(),
            message: err.to_string(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct RequestConfig {
    method: String,
    url: String,
    headers: HashMap<String, String>,
    body: Option<String>,
    user_agent: String,
}

#[derive(Debug, Clone)]
struct RetrySettings {
    max_retries: u32,
    backoff_factor: f32,
}

impl Default for RetrySettings {
    fn default() -> Self {
        RetrySettings {
            max_retries: 3,
            backoff_factor: 2.0,
        }
    }
}

async fn make_request(
    client: reqwest::Client,
    config: RequestConfig,
    retry_settings: &RetrySettings,
) -> Result<Value, RequestError> {
    let mut attempts = 0;
    loop {
        attempts += 1;

        let mut request_builder = match config.method.as_str() {
            "GET" => client.get(&config.url),
            "POST" => client.post(&config.url),
            "PUT" => client.put(&config.url),
            "DELETE" => client.delete(&config.url),
            _ => client.get(&config.url), // Default to GET if method is not recognized
        };

        let header_map: HeaderMap = config
            .headers
            .iter()
            .map(|(k, v)| {
                let name = reqwest::header::HeaderName::from_bytes(k.as_bytes()).unwrap();
                let value = reqwest::header::HeaderValue::from_str(v).unwrap();
                (name, value)
            })
            .collect();

        request_builder = request_builder.headers(header_map).header(reqwest::header::USER_AGENT, config.user_agent.clone());

        if let Some(body) = config.body.clone() {
            request_builder = request_builder.body(body);
        }

        let start = Instant::now();
        let response = request_builder.send().await;
        let elapsed = start.elapsed();

        match response {
            Ok(response) => {
                let status = response.status();
                if !status.is_success() {
                    let error_text = response.text().await?;
                    if attempts > retry_settings.max_retries {
                        return Err(RequestError {
                            status,
                            message: format!("Retry limit exceeded. Last error: {}", error_text),
                        });
                    } else {
                        debug!("Request failed with status {}. Retrying...", status);
                        let delay = Duration::from_secs_f32(retry_settings.backoff_factor.powi(attempts as i32));
                        sleep(delay).await;
                        continue;
                    }
                }

                let json: Value = response.json().await?;
                debug!("Request time: {:?}", elapsed);
                return Ok(json);
            }
            Err(err) => {
                if attempts > retry_settings.max_retries {
                    return Err(RequestError::from(err));
                } else {
                    debug!("Request failed: {}. Retrying...", err);
                    let delay = Duration::from_secs_f32(retry_settings.backoff_factor.powi(attempts as i32));
                    sleep(delay).await;
                    continue;
                }
            }
        }
    }
}


async fn make_requests(
    client: reqwest::Client,
    requests_config: Vec<RequestConfig>,
    retry_settings: &RetrySettings,
) -> Vec<Result<Value, RequestError>> {
    let futures = requests_config.into_iter().map(|config| {
        let client = client.clone();
        let retry_settings = retry_settings.clone();
        async move {
            make_request(client, config, &retry_settings).await
        }
    });

    join_all(futures).await
}

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// Number of requests to make (if no specific requests are provided)
    #[clap(short, long, default_value_t = 100)]
    num_requests: usize,

    /// Request method (if no specific requests are provided)
    #[clap(long, default_value = "GET")]
    method: String,

    /// Base URL (if no specific requests are provided)
    #[clap(long, default_value = "https://localhost:8000/test")]
    base_url: String,

    /// User agent (if no specific requests are provided)
    #[clap(long, default_value = "MyRustApp/1.0")]
    user_agent: String,

    /// Content type header (if no specific requests are provided)
    #[clap(long, default_value = "application/json")]
    content_type: String,

    /// JSON file containing request configurations
    #[clap(long, value_parser)]
    request_file: Option<String>,

     /// Max retries for a request
    #[clap(long, default_value_t = 3)]
    max_retries: u32,

    /// Backoff factor for retries
    #[clap(long, default_value_t = 2.0)]
    backoff_factor: f32,
}


#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    env_logger::init();

    let args = Args::parse();

    // Load the certificate.
    let cert = "./ssl/cert.pem";
    let cert = std::fs::read(cert).unwrap();
    let cert = reqwest::Certificate::from_pem(&cert).expect("Fail to create cert.");

    // Build the client.
    let client = reqwest::Client::builder()
        .use_rustls_tls()
        .add_root_certificate(cert)
        .pool_max_idle_per_host(100)
        .build()
        .expect("Fail to build client.");

    let requests_config = match args.request_file {
        Some(file_path) => {
            // Load request configurations from file
            let file = std::fs::File::open(file_path)?;
            let reader = std::io::BufReader::new(file);
            let request_configs: Vec<RequestConfig> = serde_json::from_reader(reader)?;
            request_configs
        }
        None => {
            // Use default request configuration
            let mut default_headers_map = HashMap::new();
            default_headers_map.insert("Content-Type".to_string(), args.content_type.clone());

            (0..args.num_requests)
                .map(|_| RequestConfig {
                    method: args.method.clone(),
                    url: args.base_url.clone(),
                    headers: default_headers_map.clone(),
                    body: None,
                    user_agent: args.user_agent.clone(),
                })
                .collect()
        }
    };

    let retry_settings = RetrySettings {
        max_retries: args.max_retries,
        backoff_factor: args.backoff_factor,
    };

    // Make the requests.
    let start_time = Instant::now();
    let results = make_requests(client, requests_config, &retry_settings).await;
    let total_duration = start_time.elapsed();

    let mut success_count = 0;
    let mut error_count = 0;

    // Iterate over the results and print each JSON response.
    for (i, result) in results.into_iter().enumerate() {
        match result {
            Ok(json) => {
                success_count += 1;
                info!("Response {}: {:#?}", i + 1, json);
            }
            Err(e) => {
                error_count += 1;
                error!("Request {} failed: {}", i + 1, e);
            }
        }
    }

    let avg_request_time = if success_count > 0 {
        total_duration / success_count as u32
    } else {
        Duration::new(0, 0)
    };

    info!("----------------------------------");
    info!("Total requests: {}", args.num_requests);
    info!("Successes: {}", success_count);
    info!("Errors: {}", error_count);
    info!("Total duration: {:?}", total_duration);
    info!("Average request time: {:?}", avg_request_time);
    info!("Throughput: {:.2} requests/second", args.num_requests as f64 / total_duration.as_secs_f64());
    info!("----------------------------------");

    Ok(())
}