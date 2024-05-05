import socket
from opentelemetry.sdk.resources import Resource, ResourceDetector

class LocalMachineResourceDetector(ResourceDetector):

    def detect(self) -> "Resource":
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)

        return Resource.create({
                    "net.host.name": hostname,
                    "net.host.ip": ip,}
                )

