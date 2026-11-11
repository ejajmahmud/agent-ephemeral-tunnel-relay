"""Core Ephemeral Tunnel Relay implementation."""
import hashlib
import hmac
import time
import uuid
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

@dataclass
class TunnelMessage:
    tunnel_id: str
    sender: str
    payload: bytes
    timestamp: float

@dataclass
class TunnelSession:
    tunnel_id: str
    target_local_port: int
    secret_token: str
    expires_at: float
    is_active: bool = True

class TunnelRelay:
    """Brokers ephemeral, authenticated tunnels between edge agents and cloud swarms."""
    
    def __init__(self, default_ttl_seconds: float = 300.0):
        self.default_ttl = default_ttl_seconds
        self.active_tunnels: Dict[str, TunnelSession] = {}

    def create_tunnel(self, local_port: int, secret_token: str) -> TunnelSession:
        tunnel_id = f"tun_{uuid.uuid4().hex[:12]}"
        session = TunnelSession(
            tunnel_id=tunnel_id,
            target_local_port=local_port,
            secret_token=secret_token,
            expires_at=time.time() + self.default_ttl
        )
        self.active_tunnels[tunnel_id] = session
        return session

    def relay_message(self, tunnel_id: str, auth_token: str, raw_payload: bytes) -> Optional[TunnelMessage]:
        session = self.active_tunnels.get(tunnel_id)
        if not session or not session.is_active:
            return None
        if time.time() > session.expires_at:
            session.is_active = False
            return None
        if not hmac.compare_digest(session.secret_token, auth_token):
            return None

        return TunnelMessage(
            tunnel_id=tunnel_id,
            sender="cloud_swarm",
            payload=raw_payload,
            timestamp=time.time()
        )

    def close_tunnel(self, tunnel_id: str) -> bool:
        if tunnel_id in self.active_tunnels:
            self.active_tunnels[tunnel_id].is_active = False
            return True
        return False
