"""
Server Management & Port Handling
Ensures reliable server startup and cleanup
"""

import os
import socket
import subprocess
import time
import requests
from pathlib import Path


class ServerManager:
    """Manages dev server lifecycle for visual UX testing"""

    def __init__(self, site_dir: str = "_site"):
        self.site_dir = site_dir
        self.server_process = None
        self.server_port = None
        self.server_url = None

    def find_available_port(self, start: int = 8080, end: int = 8090) -> int:
        """
        Find first available port in range

        Args:
            start: Start of port range
            end: End of port range

        Returns:
            Available port number

        Raises:
            RuntimeError: If no ports available in range
        """
        for port in range(start, end + 1):
            if self._is_port_available(port):
                return port

        raise RuntimeError(
            f"No available ports in range {start}-{end}. "
            f"Kill conflicting processes or expand range."
        )

    def _is_port_available(self, port: int) -> bool:
        """Check if port is available"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("localhost", port))
                return True
            except OSError:
                return False

    def kill_port(self, port: int) -> bool:
        """
        Kill any process using the specified port

        Args:
            port: Port number to free

        Returns:
            True if process was killed, False if port was already free
        """
        try:
            # Find process using port
            result = subprocess.run(
                ["lsof", "-ti", f":{port}"],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.stdout.strip():
                pids = result.stdout.strip().split("\n")
                for pid in pids:
                    try:
                        os.kill(int(pid), 9)  # SIGKILL
                        print(f"   🔪 Killed process {pid} on port {port}")
                    except ProcessLookupError:
                        pass  # Process already dead
                time.sleep(0.5)  # Let OS clean up
                return True
            return False

        except subprocess.TimeoutExpired:
            print(f"   ⚠️  Timeout checking port {port}")
            return False
        except Exception as e:
            print(f"   ⚠️  Error killing port {port}: {e}")
            return False

    def start_server(
        self,
        port: int = None,
        kill_conflicts: bool = True,
        timeout: int = 10
    ) -> str:
        """
        Start HTTP server for the built site

        Args:
            port: Port to use (None = auto-detect)
            kill_conflicts: Kill conflicting processes if True
            timeout: Seconds to wait for server to become healthy

        Returns:
            Server URL (e.g., "http://localhost:8082")

        Raises:
            RuntimeError: If server fails to start
        """
        # Verify site directory exists
        site_path = Path(self.site_dir)
        if not site_path.exists():
            raise RuntimeError(
                f"Site directory not found: {self.site_dir}\n"
                f"Run 'npm run build' first to generate the site."
            )

        # Find or validate port
        if port is None:
            print("   🔍 Finding available port...")
            port = self.find_available_port()
            print(f"   ✅ Found available port: {port}")
        else:
            if not self._is_port_available(port):
                if kill_conflicts:
                    print(f"   ⚠️  Port {port} in use, killing process...")
                    self.kill_port(port)
                    time.sleep(1)

                    if not self._is_port_available(port):
                        raise RuntimeError(
                            f"Port {port} still in use after killing process"
                        )
                else:
                    raise RuntimeError(
                        f"Port {port} is not available. "
                        f"Set kill_conflicts=True to auto-kill."
                    )

        # Start server
        print(f"   🚀 Starting HTTP server on port {port}...")
        try:
            self.server_process = subprocess.Popen(
                ["python3", "-m", "http.server", str(port)],
                cwd=self.site_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.server_port = port
            self.server_url = f"http://localhost:{port}"

            # Wait for server to be healthy
            if not self.wait_for_server(timeout=timeout):
                self.stop_server()
                raise RuntimeError(
                    f"Server failed to respond within {timeout} seconds"
                )

            print(f"   ✅ Server ready at {self.server_url}")
            return self.server_url

        except Exception as e:
            if self.server_process:
                self.stop_server()
            raise RuntimeError(f"Failed to start server: {e}")

    def wait_for_server(self, timeout: int = 10) -> bool:
        """
        Wait for server to become healthy

        Args:
            timeout: Maximum seconds to wait

        Returns:
            True if server responds, False otherwise
        """
        if not self.server_url:
            return False

        print(f"   ⏳ Waiting for server to respond...")
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                response = requests.get(self.server_url, timeout=1)
                if response.status_code == 200:
                    return True
            except requests.exceptions.RequestException:
                pass

            time.sleep(0.5)

        return False

    def health_check(self, url: str = None) -> bool:
        """
        Check if server is responding

        Args:
            url: URL to check (defaults to server_url)

        Returns:
            True if server is healthy
        """
        check_url = url or self.server_url
        if not check_url:
            return False

        try:
            response = requests.get(check_url, timeout=2)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def stop_server(self) -> None:
        """Stop the HTTP server if running"""
        if self.server_process:
            print(f"   🛑 Stopping server on port {self.server_port}...")
            try:
                self.server_process.terminate()
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_process.kill()
                self.server_process.wait()
            except Exception as e:
                print(f"   ⚠️  Error stopping server: {e}")
            finally:
                self.server_process = None
                self.server_port = None
                self.server_url = None

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures cleanup"""
        self.stop_server()


def kill_docker_port_conflicts():
    """
    Kill Docker containers that might be using common web ports

    This is a aggressive cleanup for development environments.
    Only use if you know what you're doing!
    """
    try:
        # Get running containers
        result = subprocess.run(
            ["docker", "ps", "-q"],
            capture_output=True,
            text=True,
            timeout=5
        )

        container_ids = result.stdout.strip().split("\n")
        if container_ids and container_ids[0]:
            print(f"   🐳 Found {len(container_ids)} running Docker containers")

            # Check each container for port conflicts
            for container_id in container_ids:
                port_result = subprocess.run(
                    ["docker", "port", container_id],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                # Check if using ports 8080-8090
                for line in port_result.stdout.split("\n"):
                    if any(f":{port}" in line for port in range(8080, 8091)):
                        print(
                            f"   🛑 Stopping container {container_id[:12]} "
                            f"(port conflict)"
                        )
                        subprocess.run(
                            ["docker", "stop", container_id],
                            capture_output=True,
                            timeout=10
                        )

    except subprocess.TimeoutExpired:
        print("   ⚠️  Docker check timed out")
    except FileNotFoundError:
        pass  # Docker not installed, skip
    except Exception as e:
        print(f"   ⚠️  Docker cleanup error: {e}")
