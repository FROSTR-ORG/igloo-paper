from __future__ import annotations

import json
import socket
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


DEFAULT_ENDPOINT = "http://127.0.0.1:29979/mcp"


class PaperMCPError(RuntimeError):
    pass


@dataclass
class PaperClient:
    endpoint: str = DEFAULT_ENDPOINT
    session_id: str | None = None
    next_id: int = 1

    def initialize(self) -> None:
        payload = {
            "jsonrpc": "2.0",
            "id": self._take_id(),
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "igloo-paper-export", "version": "0.1.0"},
            },
        }
        response = self._request(payload)
        if not response or "result" not in response:
            raise PaperMCPError("Paper MCP initialize failed")
        self._request({"jsonrpc": "2.0", "method": "notifications/initialized"})
        self.call_tool("get_guide", {"topic": "paper-mcp-instructions"})

    def call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = {
            "jsonrpc": "2.0",
            "id": self._take_id(),
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments or {}},
        }
        try:
            response = self._request(payload)
        except PaperMCPError as exc:
            raise PaperMCPError(f"Paper tool {name} failed while calling MCP: {exc}") from exc
        if response is None:
            raise PaperMCPError(f"Paper tool {name} returned an empty response")
        if response.get("error"):
            raise PaperMCPError(f"Paper tool {name} failed: {response['error']}")
        result = response["result"]
        if result.get("isError"):
            detail = self._content_text(result)
            raise PaperMCPError(f"Paper tool {name} returned an error: {detail}")
        return result

    def _content_text(self, result: dict[str, Any]) -> str:
        texts = [
            item.get("text", "")
            for item in result.get("content", [])
            if isinstance(item, dict) and item.get("type") == "text"
        ]
        return " ".join(text for text in texts if text).strip() or "no error detail"

    def get_basic_info(self) -> dict[str, Any]:
        content = self.call_tool("get_basic_info")["content"][0]["text"]
        return json.loads(content)

    def get_node_info_text(self, node_id: str) -> str:
        return self.call_tool("get_node_info", {"nodeId": node_id})["content"][0]["text"]

    def get_node_info(self, node_id: str) -> dict[str, Any]:
        return json.loads(self.get_node_info_text(node_id))

    def get_tree_summary(self, node_id: str, depth: int) -> str:
        content = self.call_tool("get_tree_summary", {"nodeId": node_id, "depth": depth})["content"][0]["text"]
        return json.loads(content)["summary"]

    def get_jsx(self, node_id: str, fmt: str = "tailwind") -> str:
        raw = self.call_tool("get_jsx", {"nodeId": node_id, "format": fmt})["content"][0]["text"]
        return json.loads(raw)

    def get_children(self, node_id: str) -> dict[str, Any]:
        content = self.call_tool("get_children", {"nodeId": node_id})["content"][0]["text"]
        return json.loads(content)

    def get_computed_styles(self, node_ids: list[str]) -> dict[str, Any]:
        content = self.call_tool("get_computed_styles", {"nodeIds": node_ids})["content"][0]["text"]
        return json.loads(content)

    def get_screenshot(self, node_id: str, scale: int = 1, transparent: bool = True) -> tuple[str, str]:
        last_error: PaperMCPError | None = None
        for attempt in range(2):
            try:
                content = self.call_tool(
                    "get_screenshot",
                    {"nodeId": node_id, "scale": scale, "transparent": transparent},
                )["content"][0]
                break
            except PaperMCPError as exc:
                last_error = exc
                if attempt == 0 and "timed out" in str(exc).lower():
                    continue
                raise PaperMCPError(
                    f"Paper screenshot for {node_id} (scale={scale}, transparent={transparent}) failed: {exc}"
                ) from exc
        else:
            raise PaperMCPError(
                f"Paper screenshot for {node_id} (scale={scale}, transparent={transparent}) failed: {last_error}"
            ) from last_error

        encoded = content.get("data")
        if not encoded:
            raise PaperMCPError(
                f"Paper screenshot for {node_id} (scale={scale}, transparent={transparent}) did not include image data"
            )
        mime_type = content.get("mimeType")
        if not mime_type and content.get("type") == "image":
            mime_type = "image/png"
        if not mime_type:
            raise PaperMCPError(
                f"Paper screenshot for {node_id} (scale={scale}, transparent={transparent}) did not include a MIME type"
            )
        return mime_type, encoded

    def _take_id(self) -> int:
        current = self.next_id
        self.next_id += 1
        return current

    def _request(self, payload: dict[str, Any]) -> dict[str, Any] | None:
        headers = {
            "content-type": "application/json",
            "accept": "application/json, text/event-stream",
        }
        if self.session_id:
            headers["mcp-session-id"] = self.session_id

        request = urllib.request.Request(
            self.endpoint,
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers=headers,
        )

        try:
            with urllib.request.urlopen(request, timeout=300) as response:
                if not self.session_id:
                    self.session_id = response.headers.get("mcp-session-id") or response.headers.get("Mcp-Session-Id")
                body = response.read()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")
            raise PaperMCPError(f"HTTP {exc.code} from Paper MCP: {detail}") from exc
        except (TimeoutError, socket.timeout) as exc:
            raise PaperMCPError("Timed out waiting for Paper MCP response") from exc
        except urllib.error.URLError as exc:
            if isinstance(exc.reason, socket.timeout):
                raise PaperMCPError("Timed out waiting for Paper MCP response") from exc
            raise

        text = body.decode("utf-8", "replace").strip()
        if not text or text == "null":
            return None

        for block in text.split("\n\n"):
            for line in block.splitlines():
                if line.startswith("data: "):
                    return json.loads(line[6:])

        raise PaperMCPError(f"Unable to parse MCP response: {text[:300]}")
