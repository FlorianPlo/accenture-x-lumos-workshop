"""Web UI (standard library only).

Routes:

* ``/`` and ``/?month=YYYY-MM`` - billing run overview for one month
* ``/invoice/<customer_id>/<YYYY-MM>`` - invoice page for one customer

Routing is done in :func:`route`, which is pure and unit-tested. The HTTP
server in :func:`serve` only forwards requests to it.
"""

from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from wattwise import views
from wattwise.repository import DataRepository
from wattwise.service import (
    available_months,
    billing_overview,
    billing_result,
    previous_month,
)


@dataclass(frozen=True)
class Response:
    """An HTTP response produced by :func:`route`."""

    status: int
    body: str


def route(repo: DataRepository, path: str) -> Response:
    """Turn a request path into a response.

    Args:
        repo: Data access.
        path: Request path including query string, e.g. ``"/?month=2026-11"``.

    Returns:
        The response to send.
    """
    url = urlparse(path)
    parts = [p for p in url.path.split("/") if p]
    months = available_months(repo)

    if not parts:
        month = parse_qs(url.query).get("month", [months[-1]])[0]
        if month not in months:
            return Response(404, views.render_not_found(f"No billing data for {month}"))
        return Response(200, views.render_dashboard(month, months, billing_overview(repo, month)))

    if len(parts) == 3 and parts[0] == "invoice":
        customer_id, month = parts[1], parts[2]
        if customer_id not in {c.customer_id for c in repo.customers()}:
            return Response(404, views.render_not_found(f"Unknown customer {customer_id}"))
        if month not in months:
            return Response(404, views.render_not_found(f"No billing data for {month}"))
        result = billing_result(repo, customer_id, month)
        prev = previous_month(month)
        previous = billing_result(repo, customer_id, prev) if prev in months else None
        return Response(200, views.render_invoice(month, months, result, previous))

    return Response(404, views.render_not_found(f"No page at {url.path}"))


def serve(repo: DataRepository, port: int = 8000) -> None:
    """Start the web UI and block until interrupted (Ctrl+C)."""

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802 (name required by http.server)
            if self.path == "/favicon.ico":
                self.send_response(204)
                self.end_headers()
                return
            response = route(repo, self.path)
            payload = response.body.encode("utf-8")
            self.send_response(response.status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"WattWise Billing running on http://localhost:{port}  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()
