use axum::{http::StatusCode, response::IntoResponse, Json};
use serde::{Deserialize, Serialize};
use serde_json::Value;

pub async fn process_data(Json(request): Json<DataRequest>) -> impl IntoResponse {
    // Calculate sums and return response

    let mut string_len = 0;
    let mut int_sum = 0;

    for item in &request.data {
        match item {
            Value::String(s) => string_len += s.len(),
            Value::Number(n) => {
                // Would be better using ? to propogate a failure to convert number
                if let Some(i) = n.as_i64() {
                    int_sum += i;
                }
            }
            _ => {
                // Should replace with error variant or can do nothing to ignore
                unreachable!()
            }
        }
    }

    let response = DataResponse {
        string_len,
        int_sum,
    };

    (StatusCode::OK, Json(response))
}

#[derive(Deserialize)]
pub struct DataRequest {
    data: Vec<Value>,
}

#[derive(Serialize)]
pub struct DataResponse {
    string_len: usize,
    int_sum: i64,
}
