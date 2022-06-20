import ssl
import sys
from collections import deque
from collections.abc import Callable
from enum import Enum
from typing import Any, ClassVar
from typing_extensions import Literal, TypeAlias

from . import constants, events, futures, protocols, transports

def _create_transport_context(server_side: bool, server_hostname: str | None) -> ssl.SSLContext: ...

if sys.version_info >= (3, 11):
    SSLAgainErrors: tuple[type[ssl.SSLWantReadError], type[ssl.SSLSyscallError]]

    class SSLProtocolState(Enum):
        UNWRAPPED: str
        DO_HANDSHAKE: str
        WRAPPED: str
        FLUSHING: str
        SHUTDOWN: str

    class AppProtocolState(Enum):
        STATE_INIT: str
        STATE_CON_MADE: str
        STATE_EOF: str
        STATE_CON_LOST: str
    def add_flowcontrol_defaults(high: int | None, low: int | None, kb: int) -> tuple[int, int]: ...

else:
    _UNWRAPPED: Literal["UNWRAPPED"]
    _DO_HANDSHAKE: Literal["DO_HANDSHAKE"]
    _WRAPPED: Literal["WRAPPED"]
    _SHUTDOWN: Literal["SHUTDOWN"]

class _SSLPipe:

    max_size: ClassVar[int]

    _context: ssl.SSLContext
    _server_side: bool
    _server_hostname: str | None
    _state: str
    _incoming: ssl.MemoryBIO
    _outgoing: ssl.MemoryBIO
    _sslobj: ssl.SSLObject | None
    _need_ssldata: bool
    _handshake_cb: Callable[[BaseException | None], None] | None
    _shutdown_cb: Callable[[], None] | None
    def __init__(self, context: ssl.SSLContext, server_side: bool, server_hostname: str | None = ...) -> None: ...
    @property
    def context(self) -> ssl.SSLContext: ...
    @property
    def ssl_object(self) -> ssl.SSLObject | None: ...
    @property
    def need_ssldata(self) -> bool: ...
    @property
    def wrapped(self) -> bool: ...
    def do_handshake(self, callback: Callable[[BaseException | None], None] | None = ...) -> list[bytes]: ...
    def shutdown(self, callback: Callable[[], None] | None = ...) -> list[bytes]: ...
    def feed_eof(self) -> None: ...
    def feed_ssldata(self, data: bytes, only_handshake: bool = ...) -> tuple[list[bytes], list[bytes]]: ...
    def feed_appdata(self, data: bytes, offset: int = ...) -> tuple[list[bytes], int]: ...

class _SSLProtocolTransport(transports._FlowControlMixin, transports.Transport):

    _sendfile_compatible: ClassVar[constants._SendfileMode]

    _loop: events.AbstractEventLoop
    _ssl_protocol: SSLProtocol
    _closed: bool
    def __init__(self, loop: events.AbstractEventLoop, ssl_protocol: SSLProtocol) -> None: ...
    def get_extra_info(self, name: str, default: Any | None = ...) -> dict[str, Any]: ...
    def set_protocol(self, protocol: protocols.BaseProtocol) -> None: ...
    def get_protocol(self) -> protocols.BaseProtocol: ...
    def is_closing(self) -> bool: ...
    def close(self) -> None: ...
    if sys.version_info >= (3, 7):
        def is_reading(self) -> bool: ...

    def pause_reading(self) -> None: ...
    def resume_reading(self) -> None: ...
    def set_write_buffer_limits(self, high: int | None = ..., low: int | None = ...) -> None: ...
    def get_write_buffer_size(self) -> int: ...
    if sys.version_info >= (3, 7):
        @property
        def _protocol_paused(self) -> bool: ...

    def write(self, data: bytes) -> None: ...
    def can_write_eof(self) -> Literal[False]: ...
    def abort(self) -> None: ...
    if sys.version_info >= (3, 11):
        def get_write_buffer_limits(self) -> tuple[int, int]: ...
        def get_read_buffer_limits(self) -> tuple[int, int]: ...
        def set_read_buffer_limits(self, high: int | None = ..., low: int | None = ...) -> None: ...
        def get_read_buffer_size(self) -> int: ...

if sys.version_info >= (3, 11):
    _SSLProtocolBase: TypeAlias = protocols.BufferedProtocol
else:
    _SSLProtocolBase: TypeAlias = protocols.Protocol

class SSLProtocol(_SSLProtocolBase):
    if sys.version_info >= (3, 11):
        max_size: ClassVar[int]

    _server_side: bool
    _server_hostname: str | None
    _sslcontext: ssl.SSLContext
    _extra: dict[str, Any]
    _write_backlog: deque[tuple[bytes, int]]
    _write_buffer_size: int
    _waiter: futures.Future[Any]
    _loop: events.AbstractEventLoop
    _app_transport: _SSLProtocolTransport
    _sslpipe: _SSLPipe | None
    _session_established: bool
    _in_handshake: bool
    _in_shutdown: bool
    _transport: transports.BaseTransport | None
    _call_connection_made: bool
    _ssl_handshake_timeout: int | None
    _app_protocol: protocols.BaseProtocol
    _app_protocol_is_buffer: bool

    if sys.version_info >= (3, 11):
        def __init__(
            self,
            loop: events.AbstractEventLoop,
            app_protocol: protocols.BaseProtocol,
            sslcontext: ssl.SSLContext,
            waiter: futures.Future[Any],
            server_side: bool = ...,
            server_hostname: str | None = ...,
            call_connection_made: bool = ...,
            ssl_handshake_timeout: int | None = ...,
            ssl_shutdown_timeout: float | None = ...,
        ) -> None: ...
    elif sys.version_info >= (3, 7):
        def __init__(
            self,
            loop: events.AbstractEventLoop,
            app_protocol: protocols.BaseProtocol,
            sslcontext: ssl.SSLContext,
            waiter: futures.Future[Any],
            server_side: bool = ...,
            server_hostname: str | None = ...,
            call_connection_made: bool = ...,
            ssl_handshake_timeout: int | None = ...,
        ) -> None: ...
    else:
        def __init__(
            self,
            loop: events.AbstractEventLoop,
            app_protocol: protocols.BaseProtocol,
            sslcontext: ssl.SSLContext,
            waiter: futures.Future[Any],
            server_side: bool = ...,
            server_hostname: str | None = ...,
            call_connection_made: bool = ...,
        ) -> None: ...
    if sys.version_info >= (3, 7):
        def _set_app_protocol(self, app_protocol: protocols.BaseProtocol) -> None: ...

    def _wakeup_waiter(self, exc: BaseException | None = ...) -> None: ...
    def connection_made(self, transport: transports.BaseTransport) -> None: ...
    def connection_lost(self, exc: BaseException | None) -> None: ...
    def pause_writing(self) -> None: ...
    def resume_writing(self) -> None: ...
    def eof_received(self) -> None: ...
    def _get_extra_info(self, name: str, default: Any | None = ...) -> Any: ...
    def _start_shutdown(self) -> None: ...
    if sys.version_info >= (3, 11):
        def _write_appdata(self, list_of_data: list[bytes]) -> None: ...
    else:
        def _write_appdata(self, data: bytes) -> None: ...

    def _start_handshake(self) -> None: ...
    if sys.version_info >= (3, 7):
        def _check_handshake_timeout(self) -> None: ...

    def _on_handshake_complete(self, handshake_exc: BaseException | None) -> None: ...
    def _fatal_error(self, exc: BaseException, message: str = ...) -> None: ...
    def _abort(self) -> None: ...
    if sys.version_info >= (3, 11):
        def buffer_updated(self, nbytes: int) -> None: ...
        def get_buffer(self, n: int) -> memoryview: ...
    else:
        def _finalize(self) -> None: ...
        def _process_write_backlog(self) -> None: ...
        def data_received(self, data: bytes) -> None: ...
