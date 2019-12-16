from typing import Dict, Callable, Optional, Any, List, Tuple, Union
import logging

logger = logging.getLogger("resp")

RedisValue = Union[int, str, Optional[bytes]]
SEP_LENGTH = len(b'\r\n')


class RespError(Exception):
    pass


def parse_simple_string(data: bytes) -> Tuple[str, bytes]:
    data, buf = data.split(b'\r\n', 1)
    return data.decode(), buf


def parse_error(data: bytes) -> Tuple[str, bytes]:
    data, buf = data.split(b'\r\n', 1)
    return data.decode(), buf


def parse_int(data: bytes) -> Tuple[int, bytes]:
    data, buf = data.split(b'\r\n', 1)
    return int(data), buf


def parse_bulk_string(data: bytes) -> Tuple[Optional[bytes], bytes]:
    encoded_length, data = data.split(b'\r\n', 1)
    length = int(encoded_length)

    if length == -1:
        return None, data

    data, buf = data[:length], data[length + SEP_LENGTH:]
    return data, buf


def parse_array(data: bytes) -> Tuple[Optional[List[RedisValue]], bytes]:
    encoded_length, data = data.split(b'\r\n', 1)
    length = int(encoded_length)

    logger.debug("parse_array: length=%s", length)

    if length == -1:
        return None, data

    elems: List[Any] = []

    for i in range(length):
        logger.debug("parse_array: data=%s", data)
        elem, data = parse_resp(data)
        logger.debug("parse_array: elem=%s", elem)
        elems.append(elem)

    return elems, data


PARSERS: Dict[bytes, Callable] = {
    b'+': parse_simple_string,
    b'$': parse_bulk_string,
    b'-': parse_error,
    b':': parse_int,
    b'*': parse_array,
}


def parse_resp(data: bytes):
    assert type(data) == bytes

    if len(data) < 2:
        raise Exception(f"Invalid data: {data!r}")

    parse = PARSERS[data[0:1]]
    return parse(data[1:])


def parse(data: bytes):
    response, _remaining_data = parse_resp(data)
    return response
