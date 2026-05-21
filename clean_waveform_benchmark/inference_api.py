#!/usr/bin/env python3
"""
Simple HTTP API for fill-level inference.
Uses the same logic as inference_demo.py but exposed via a web interface.
"""

import json
import http.server
import socketserver
import sys
from pathlib import Path

# Add current directory to path so we can import from inference_demo
sys.path.append(str(Path(__file__).parent))

from inference_demo import KNearestNeighbors, load_rows

# Pre-train models on startup
DATA_PATH = Path(__file__).parent / "clean_waveform_dataset.json"

try:
    rows = load_rows(DATA_PATH)
    train_rows = [r for r in rows if r["variant_role"] == "noisy_variant"]
    site_model = KNearestNeighbors("site_class", k=5).fit(train_rows)
    fill_model = KNearestNeighbors("fill_state", k=5).fit(train_rows)
    EXAMPLE_ROW = train_rows[0]
except Exception as e:
    print(f"Error loading data: {e}")
    sys.exit(1)

class InferenceHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            self.send_error(400, "Empty request body")
            return
            
        post_data = self.rfile.read(content_length)
        try:
            input_data = json.loads(post_data)
            
            # Ensure the input has the expected 'features' structure
            if "features" not in input_data:
                self.send_error(400, "Missing 'features' key in request body")
                return

            site_pred, site_conf, _ = site_model.predict_one(input_data)
            fill_pred, fill_conf, _ = fill_model.predict_one(input_data)
            
            response = {
                "predicted_site_class": site_pred,
                "site_confidence": round(site_conf, 3),
                "predicted_fill_state": fill_pred,
                "fill_confidence": round(fill_conf, 3),
                "recommended_action": "Schedule Service" if fill_pred == "full" else "Continue Monitoring"
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except Exception as e:
            self.send_error(400, f"Error processing request: {str(e)}")

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "ready",
            "description": "Industrial Telemetry Inference API",
            "endpoints": {
                "POST /": "Send JSON with 'features' key to get inference"
            },
            "example_input": {
                "features": EXAMPLE_ROW["features"]
            }
        }, indent=2).encode('utf-8'))

if __name__ == "__main__":
    PORT = 8080
    # Enable address reuse to avoid 'Address already in use' errors on restart
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), InferenceHandler) as httpd:
        print(f"Inference API serving at http://localhost:{PORT}")
        print("Test with: curl -X POST -d '{\"features\": {...}}' http://localhost:8080")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.server_close()
