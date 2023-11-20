from os.path import isfile
def encode(hex_string: str) -> str:
    assert isinstance(hex_string, str), "hex string must be a string"
    return "".join(chr(0x100 + int(hex_string[i : i + 2], 0x10)) for i in range(0, len(hex_string), 2))
def decode(encoded_string: str) -> str:
    assert isinstance(encoded_string, str), "x must be a string"
    return "".join("%.2x" % (ord(i) - 0x100) for i in encoded_string)
def encode_hex(hex_value: int) -> str:
    assert isinstance(hex_value, int), "x must be an integer"
    return encode("%x" % hex_value)
def decode_hex(encoded_string: str) -> int:
    assert isinstance(encoded_string, str), "x must be a string"
    return int(decode(encoded_string), 0x10)
def encode_file(file_path: str) -> str:
    assert isinstance(file_path, str), "x must be a string"
    assert isfile(file_path), "x must be a file"
    return encode("".join("%.2x" % i for i in open(file_path, "rb").read()))
def decode_file(encoded_string: str, filepath: str) -> None:
    assert isinstance(encoded_string, str), "x must be a string"
    open(filepath, "wb").write(bytes.fromhex(decode(encoded_string)))
def encode_string(string: str, encoding: str = "utf-8") -> str:
    assert isinstance(string, str), "x must be a string"
    return encode("".join("%.2x" % i for i in string.encode(encoding)))
def decode_string(encoded_string: str, encoding: str = "utf-8") -> str:
    assert isinstance(encoded_string, str), "x must be a string"
    return bytes.fromhex(decode(encoded_string)).decode(encoding)
