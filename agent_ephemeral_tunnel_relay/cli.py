"""CLI for agent-ephemeral-tunnel-relay."""
import sys
import argparse
from .relay import TunnelRelay

def main():
    parser = argparse.ArgumentParser(description="Agent Ephemeral Tunnel Relay CLI")
    parser.add_argument("--demo", action="store_true", help="Create and test ephemeral tunnel")
    args = parser.parse_args()

    if args.demo:
        relay = TunnelRelay()
        session = relay.create_tunnel(local_port=8080, secret_token="auth_secret_99")
        print(f"Created tunnel: ID={session.tunnel_id}, TargetPort={session.target_local_port}")
        msg = relay.relay_message(session.tunnel_id, "auth_secret_99", b"GET /health HTTP/1.1")
        print(f"Relayed message successfully: {msg.payload.decode()}")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
