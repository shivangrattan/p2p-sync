from dataclasses import dataclass, field
from pathlib import Path
from ipaddress import IPV4Address

@dataclass(frozen=True)
class NetworkConfig:
    host: IPV4Address
    port: int

    def __post_init__(self) -> None:
        if not 1 <= self.port <= 65535:
            raise ValueError("Port must be between 1 and 65535")


default_listener_config = NetworkConfig(host="127.0.0.1", port=9000)

@dataclass
class AppConfig(frozen=True):
    shared_directory: Path # synced directory
    listener_config: NetworkConfig = field(default = default_listener_config) # ipv4 and port for listener
    remote_config: NetworkConfig # ipv4 and port for remote
    chunk_size: int = 1 # chunk size in MiB
    max_control_message_size: int = 1 # maximum accepted control-message size

    def __post_init__(self) -> None:
    if not self.shared_directory.exists():
        raise ValueError(
            f"The path does not exist: {self.shared_directory}"
        )

    if not self.shared_directory.is_dir():
        raise ValueError(
            f"The path is not a directory: {self.shared_directory}"
        )
    
    