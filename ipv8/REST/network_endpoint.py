from __future__ import absolute_import

from base64 import b64encode
import json

from twisted.web import resource


class NetworkEndpoint(resource.Resource):
    """
    This endpoint is responsible for handing all requests regarding the state of the network.
    """

    def __init__(self, session):
        resource.Resource.__init__(self)
        self.session = session

    def render_peers(self):
        network = self.session.network
        peer_list = network.verified_peers[:]
        return {
                b64encode(peer.mid): {
                            "ip": peer.address[0],
                            "port": peer.address[1],
                            "public_key": b64encode(peer.public_key.key_to_bin()),
                            "services": [b64encode(s) for s in network.get_services_for_peer(peer)]
                }
            for peer in peer_list
        }

    def render_GET(self, request):
        return json.dumps({"peers": self.render_peers()})
