from asyncredis.resp import parse_resp


def test_simple_string():
    data = b'+OK\r\n'
    response = parse_resp(data)
    assert response == ('OK', b'')


def test_error():
    data = b'-ERR foo\r\n'
    response = parse_resp(data)
    assert response == ('ERR foo', b'')


def test_int():
    data = b':42\r\n'
    response = parse_resp(data)
    assert response == (42, b'')


def test_bulk_string():
    data = b"$6\r\nfoobar\r\n"
    response = parse_resp(data)
    assert response == (b'foobar', b'')


def test_bulk_string_empty():
    data = b"$0\r\n\r\n"
    response = parse_resp(data)
    assert response == (b'', b'')


def test_bulk_string_null():
    data = b"$-1\r\n"
    response = parse_resp(data)
    assert response == (None, b'')


def test_bulk_string_with_extra_data():
    data = b"$6\r\nfoobar\r\nquux"
    response = parse_resp(data)
    assert response == (b'foobar', b'quux')


def test_array():
    data = b'*2\r\n$3\r\nfoo\r\n$3\r\none\r\n'
    response = parse_resp(data)
    assert response == ([b"foo", b"one"], b'')


def test_array_null():
    data = b"*-1\r\n"
    response = parse_resp(data)
    assert response == (None, b'')


def test_array_with_null():
    data = b"""*3\r
$3\r
foo\r
$-1\r
$3\r
bar\r
"""
    response = parse_resp(data)
    assert response == ([b'foo', None, b'bar'], b'')
