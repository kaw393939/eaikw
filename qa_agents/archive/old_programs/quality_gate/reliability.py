"""
Reliability utilities for visual UX testing
Retry logic, validation, and error recovery
"""

import asyncio
import base64
import time
from functools import wraps
from typing import Callable, Any
from io import BytesIO
from PIL import Image


def retry(
    max_attempts: int = 3,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """
    Retry decorator with exponential backoff

    Args:
        max_attempts: Maximum number of retry attempts
        backoff: Backoff multiplier (delay = backoff ^ attempt)
        exceptions: Tuple of exceptions to catch and retry

    Usage:
        @retry(max_attempts=3, backoff=2.0)
        async def flaky_function():
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts:
                        delay = backoff ** attempt
                        print(
                            f"   ⚠️  Attempt {attempt} failed: {e}. "
                            f"Retrying in {delay:.1f}s..."
                        )
                        await asyncio.sleep(delay)
                    else:
                        print(
                            f"   ❌ All {max_attempts} attempts failed: {e}"
                        )

            raise last_exception

        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts:
                        delay = backoff ** attempt
                        print(
                            f"   ⚠️  Attempt {attempt} failed: {e}. "
                            f"Retrying in {delay:.1f}s..."
                        )
                        time.sleep(delay)
                    else:
                        print(
                            f"   ❌ All {max_attempts} attempts failed: {e}"
                        )

            raise last_exception

        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def validate_screenshot(screenshot_data: dict) -> tuple[bool, str]:
    """
    Validate that a screenshot is not blank or corrupted

    Args:
        screenshot_data: Dict with 'base64' key containing image data

    Returns:
        (is_valid, error_message) tuple
    """
    try:
        # Decode base64
        image_bytes = base64.b64decode(screenshot_data['base64'])

        # Open with PIL
        img = Image.open(BytesIO(image_bytes))

        # Check dimensions
        width, height = img.size
        if width < 100 or height < 100:
            return False, f"Image too small: {width}x{height}"

        # Check if mostly blank (all pixels similar color)
        # Convert to grayscale and check variance
        grayscale = img.convert('L')
        pixels = list(grayscale.getdata())

        # Calculate simple variance
        mean = sum(pixels) / len(pixels)
        variance = sum((p - mean) ** 2 for p in pixels) / len(pixels)

        # If variance is very low, image is probably blank
        if variance < 10:
            return False, "Image appears to be blank (low variance)"

        # Check file size (very small = likely corrupted)
        if len(image_bytes) < 1000:
            return False, f"Image file too small: {len(image_bytes)} bytes"

        return True, "Valid"

    except Exception as e:
        return False, f"Validation error: {e}"


def validate_all_screenshots(
    screenshots: dict[str, dict]
) -> tuple[bool, list[str]]:
    """
    Validate multiple screenshots

    Args:
        screenshots: Dict mapping names to screenshot data

    Returns:
        (all_valid, error_messages) tuple
    """
    errors = []

    for name, screenshot in screenshots.items():
        is_valid, message = validate_screenshot(screenshot)
        if not is_valid:
            errors.append(f"{name}: {message}")

    return len(errors) == 0, errors


def handle_partial_failure(
    results: list,
    min_success_rate: float = 0.5
) -> tuple[bool, list, list]:
    """
    Handle cases where some analyses succeed and others fail

    Args:
        results: List of (success, data) tuples
        min_success_rate: Minimum fraction of successes to continue

    Returns:
        (should_continue, successes, failures) tuple
    """
    successes = [r for r in results if r[0]]
    failures = [r for r in results if not r[0]]

    success_rate = len(successes) / len(results) if results else 0
    should_continue = success_rate >= min_success_rate

    return should_continue, successes, failures


def format_troubleshooting_message(error: Exception, context: dict) -> str:
    """
    Generate helpful troubleshooting message for common errors

    Args:
        error: The exception that occurred
        context: Dict with context info (url, port, etc.)

    Returns:
        Formatted troubleshooting message
    """
    error_type = type(error).__name__
    url = context.get('url', 'unknown')
    port = context.get('port', 'unknown')

    messages = {
        'ConnectionError': f"""
❌ Cannot connect to {url}

Troubleshooting:
1. Is the server running?
   → Run: cd _site && python3 -m http.server {port}

2. Check for port conflicts:
   → Run: lsof -i :{port}

3. Kill conflicting processes:
   → Run: lsof -ti:{port} | xargs kill -9

4. Or use ServerManager to handle automatically:
   → from qa_agents.server_manager import ServerManager
   → with ServerManager() as sm:
   →     url = sm.start_server(kill_conflicts=True)
        """,

        'TimeoutError': f"""
❌ Timeout waiting for {url}

Troubleshooting:
1. Server may be slow to start. Try increasing timeout.
2. Check if page has slow-loading resources.
3. Verify site built correctly:
   → Run: npm run build
   → Check: ls -la _site/index.html
        """,

        'FileNotFoundError': """
❌ Site directory not found

Troubleshooting:
1. Build the site first:
   → Run: npm run build

2. Verify _site directory exists:
   → Run: ls -la _site/

3. Check .eleventy.js output directory setting.
        """,

        'RuntimeError': f"""
❌ {str(error)}

Troubleshooting:
1. Check server logs for errors
2. Verify site built correctly: npm run build
3. Try different port: --port 8090
4. Check Docker conflicts: docker ps
        """
    }

    return messages.get(error_type, f"❌ {error_type}: {error}")


class ProgressTracker:
    """
    Track progress of long-running operations

    Usage:
        with ProgressTracker(total=10, desc="Analyzing") as progress:
            for i in range(10):
                do_work()
                progress.update(1)
    """

    def __init__(self, total: int, desc: str = "Progress"):
        self.total = total
        self.current = 0
        self.desc = desc
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        self._print_progress()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.current = self.total
            self._print_progress()
            elapsed = time.time() - self.start_time
            print(f"\n   ✅ Completed in {elapsed:.1f}s")

    def update(self, amount: int = 1):
        """Update progress by amount"""
        self.current = min(self.current + amount, self.total)
        self._print_progress()

    def _print_progress(self):
        """Print progress bar"""
        percent = (self.current / self.total) * 100 if self.total > 0 else 0
        bar_length = 40
        filled = int(bar_length * self.current / self.total)
        bar = "█" * filled + "░" * (bar_length - filled)

        elapsed = time.time() - self.start_time if self.start_time else 0
        eta = (
            (elapsed / self.current * (self.total - self.current))
            if self.current > 0
            else 0
        )

        print(
            f"\r   {self.desc}: {bar} {percent:.0f}% "
            f"({self.current}/{self.total}) "
            f"ETA: {eta:.0f}s",
            end="",
            flush=True
        )


def estimate_cost(
    num_screenshots: int,
    detail_level: str = "high",
    model: str = "gpt-4o"
) -> dict:
    """
    Estimate cost for visual UX analysis

    Args:
        num_screenshots: Number of screenshots to analyze
        detail_level: "low" or "high"
        model: Model name

    Returns:
        Dict with cost breakdown
    """
    # Token costs per image (approximate)
    token_costs = {
        "gpt-4o": {"low": 85, "high": 765},
        "gpt-4o-mini": {"low": 85, "high": 765},
        "gpt-4.1-mini": {"low": 85, "high": 765},
    }

    # Pricing per 1M tokens (input)
    pricing = {
        "gpt-4o": 2.50,
        "gpt-4o-mini": 0.15,
        "gpt-4.1-mini": 0.15,
    }

    tokens_per_image = token_costs.get(model, token_costs["gpt-4o"])[
        detail_level
    ]
    price_per_million = pricing.get(model, pricing["gpt-4o"])

    # Add text tokens (~500 per analysis)
    total_tokens = (tokens_per_image + 500) * num_screenshots

    # Calculate cost
    cost = (total_tokens / 1_000_000) * price_per_million

    return {
        "num_screenshots": num_screenshots,
        "tokens_per_screenshot": tokens_per_image + 500,
        "total_tokens": total_tokens,
        "price_per_million_tokens": price_per_million,
        "estimated_cost": cost,
    }


def print_cost_estimate(cost_info: dict):
    """Pretty print cost estimate"""
    print("\n" + "=" * 70)
    print("💰 COST ESTIMATE")
    print("=" * 70)
    print(f"   Screenshots: {cost_info['num_screenshots']}")
    print(f"   Tokens per screenshot: ~{cost_info['tokens_per_screenshot']}")
    print(f"   Total tokens: ~{cost_info['total_tokens']:,}")
    print(
        f"   Estimated cost: ${cost_info['estimated_cost']:.4f}"
    )
    print("=" * 70 + "\n")
