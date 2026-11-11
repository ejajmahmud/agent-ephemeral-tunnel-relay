"""Unit tests for agent-ephemeral-tunnel-relay."""
import time
import unittest
from agent_ephemeral_tunnel_relay.relay import TunnelRelay

class TestTunnelRelay(unittest.TestCase):
    def setUp(self):
        self.relay = TunnelRelay(default_ttl_seconds=1.0)

    def test_create_and_relay(self):
        sess = self.relay.create_tunnel(3000, "token_abc")
        msg = self.relay.relay_message(sess.tunnel_id, "token_abc", b"payload_data")
        self.assertIsNotNone(msg)
        self.assertEqual(msg.payload, b"payload_data")

    def test_invalid_auth_rejected(self):
        sess = self.relay.create_tunnel(3000, "token_abc")
        msg = self.relay.relay_message(sess.tunnel_id, "wrong_token", b"data")
        self.assertIsNone(msg)

    def test_expiry(self):
        sess = self.relay.create_tunnel(3000, "token_abc")
        time.sleep(1.1)
        msg = self.relay.relay_message(sess.tunnel_id, "token_abc", b"data")
        self.assertIsNone(msg)
