sudo cloudflared service install <cloudflare-tunnel-token>
# Have a mapping in cloudflare tunnels to the local port 8000
uvicorn api:app --host 0.0.0.0 --port 8000

