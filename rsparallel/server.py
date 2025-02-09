import asyncio
import random

from fastapi import FastAPI, HTTPException, Query

app = FastAPI()

# Global counter for in-flight requests and an async lock to protect it.
inflight_requests = 0
inflight_lock = asyncio.Lock()


@app.api_route("/test", methods=["GET", "POST", "PUT"])
async def test_endpoint(
    # Mean response time in seconds (default: 0.1 sec)
    mean_response_time: float = Query(
        0.010, description="Mean response time in seconds"
    ),
    # Standard deviation for response time (default: 0.01 sec)
    resp_time_std: float = Query(
        0.005, description="Response time standard deviation in seconds"
    ),
    # Maximum number of in-flight requests before the server responds with a 429 error
    num_inflight_before_429: int = Query(
        50, description="Number of in-flight requests allowed before returning 429"
    ),
    # Probability that the request will return a simulated 500 error.
    # Note: The query parameter is named "500_probability" for the client.
    error_500_probability: float = Query(
        0.1,
        alias="500_probability",
        description="Probability of returning a 500 error (between 0 and 1)",
    ),
):
    global inflight_requests

    # Check and update the in-flight counter atomically.
    async with inflight_lock:
        if inflight_requests >= num_inflight_before_429:
            raise HTTPException(status_code=429, detail="Too many requests in flight")
        inflight_requests += 1

    try:
        # Calculate a delay based on a normal distribution.
        delay = max(0, random.gauss(mean_response_time, resp_time_std))
        await asyncio.sleep(delay)

        # With the given probability, simulate an internal server error.
        if random.random() < error_500_probability:
            raise HTTPException(
                status_code=500, detail="Simulated Internal Server Error"
            )

        return {"message": "Success", "delay": delay}
    finally:
        # Always decrement the in-flight counter.
        async with inflight_lock:
            inflight_requests -= 1


# To run the server with: uvicorn server:app --reload
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        ssl_keyfile="./ssl/test-key.pem",
        ssl_certfile="./ssl/test-cert.pem",
        http="h2",
    )
