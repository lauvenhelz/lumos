import lumos
import pytest


@pytest.mark.parametrize("buffer,expected", [(b'\x12\x00\x00\x13\x00\x00', [(18, b''), (19, b'')]),
                                             (b'\x12\x00', []),
                                             (b'\x20\x00\x03\xff\xff\xff\x13', [(32, b'\xff\xff\xff')])])
def test_parse_command(buffer, expected):
    p = lumos.Parser()
    assert list(p.parse(buffer)) == expected


@pytest.mark.parametrize("parts,expected", [([b'\x12\x00\x00', b'\x13\x00\x00'], [(18, b''), (19, b'')]),
                                            ([b'\x12\x00\x00\x13', b'\x00\x00'], [(18, b''), (19, b'')]),
                                            ([b'\x12\x00\x00\x13', b'', b'\x00\x00'], [(18, b''), (19, b'')]),
                                            ([b'\x20\x00\x03\xff\xff', b'\xff'], [(32, b'\xff\xff\xff')])])
def test_parse_command_with_tail(parts, expected):
    p = lumos.Parser()
    result = []
    for part in parts:
        result.extend(list(p.parse(part)))
    assert result == expected
