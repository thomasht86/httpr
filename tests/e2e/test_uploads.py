"""E2E file upload tests using httpbun container."""

import tempfile
from pathlib import Path

import pytest

import httpr


@pytest.mark.e2e
class TestFileUploads:
    """Test multipart file uploads against httpbun container."""

    def test_single_file_upload(self, e2e_base_url: str, e2e_ca_cert: str, tmp_path: Path) -> None:
        """Test uploading a single file via multipart form."""
        # Create a temporary file with content
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello, httpr!")

        client = httpr.Client(ca_cert_file=e2e_ca_cert)
        response = client.post(
            f"{e2e_base_url}/any",
            files={"upload": str(test_file)},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["method"] == "POST"
        # httpbun echoes uploaded files as objects with content field
        assert "files" in data
        assert "upload" in data["files"]
        assert data["files"]["upload"]["content"] == "Hello, httpr!"

    def test_multiple_file_upload(self, e2e_base_url: str, e2e_ca_cert: str, tmp_path: Path) -> None:
        """Test uploading multiple files via multipart form."""
        # Create multiple temporary files
        file1 = tmp_path / "file1.txt"
        file1.write_text("Content of file 1")
        file2 = tmp_path / "file2.txt"
        file2.write_text("Content of file 2")

        client = httpr.Client(ca_cert_file=e2e_ca_cert)
        response = client.post(
            f"{e2e_base_url}/any",
            files={
                "first": str(file1),
                "second": str(file2),
            },
        )

        assert response.status_code == 200
        data = response.json()
        # httpbun returns file info as objects with content field
        assert data["files"]["first"]["content"] == "Content of file 1"
        assert data["files"]["second"]["content"] == "Content of file 2"

    def test_large_file_upload(self, e2e_base_url: str, e2e_ca_cert: str, tmp_path: Path) -> None:
        """Test uploading a larger file."""
        test_file = tmp_path / "large.txt"
        # Create a file with 10KB of content
        content = "x" * 10240
        test_file.write_text(content)

        client = httpr.Client(ca_cert_file=e2e_ca_cert)
        response = client.post(
            f"{e2e_base_url}/any",
            files={"largefile": str(test_file)},
        )

        assert response.status_code == 200
        data = response.json()
        # Verify the file was uploaded with correct size
        assert data["files"]["largefile"]["size"] == 10240
        assert data["files"]["largefile"]["content"] == content

    def test_binary_file_upload(self, e2e_base_url: str, e2e_ca_cert: str, tmp_path: Path) -> None:
        """Test uploading binary content."""
        binary_file = tmp_path / "binary.bin"
        # Write some binary data
        binary_content = bytes(range(256))
        binary_file.write_bytes(binary_content)

        client = httpr.Client(ca_cert_file=e2e_ca_cert)
        response = client.post(
            f"{e2e_base_url}/any",
            files={"binary": str(binary_file)},
        )

        assert response.status_code == 200
        data = response.json()
        assert "binary" in data["files"]
