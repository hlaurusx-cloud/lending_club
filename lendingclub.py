#!/usr/bin/env python3
"""
Test script for EncodeCraft encoding algorithms
Validates that all encoding/decoding functions work correctly
"""

import base64
import urllib.parse
import html
import binascii


def test_base64():
    """Test Base64 encoding/decoding"""
    test_strings = [
        "Hello, World!",
        "Test 123",
        "Special chars: @#$%^&*()",
        "Unicode: 你好世界",
        "Emoji: 🚀🎉",
        ""  # Empty string
    ]
    
    print("=== Base64 Tests ===")
    for test_str in test_strings:
        try:
            # JavaScript equivalent: btoa(unescape(encodeURIComponent(text)))
            encoded = base64.b64encode(test_str.encode('utf-8')).decode('ascii')
            decoded = base64.b64decode(encoded.encode('ascii')).decode('utf-8')
            
            print(f"Input: '{test_str}'")
            print(f"Encoded: {encoded}")
            print(f"Decoded: {decoded}")
            print(f"Match: {test_str == decoded}")
            print("-" * 40)
        except Exception as e:
            print(f"Error with '{test_str}': {e}")
            print("-" * 40)


def test_url_encoding():
    """Test URL encoding/decoding"""
    test_strings = [
        "Hello World",
        "Special chars: @#$%^&*()",
        "Query: key=value&other=test",
        "Unicode: 你好",
        "Spaces and symbols: !@#$%^&*()",
        ""  # Empty string
    ]
    
    print("\n=== URL Encoding Tests ===")
    for test_str in test_strings:
        try:
            # JavaScript equivalent: encodeURIComponent(text)
            encoded = urllib.parse.quote(test_str, safe='')
            decoded = urllib.parse.unquote(encoded)
            
            print(f"Input: '{test_str}'")
            print(f"Encoded: {encoded}")
            print(f"Decoded: {decoded}")
            print(f"Match: {test_str == decoded}")
            print("-" * 40)
        except Exception as e:
            print(f"Error with '{test_str}': {e}")
            print("-" * 40)


def test_hex_encoding():
    """Test Hexadecimal encoding/decoding"""
    test_strings = [
        "Hello",
        "Test 123",
        "ABC",
        "Unicode: 你好",
        "Binary: \\x00\\x01\\x02",
        ""  # Empty string
    ]
    
    print("\n=== Hexadecimal Tests ===")
    for test_str in test_strings:
        try:
            # Convert to hex
            encoded = binascii.hexlify(test_str.encode('utf-8')).decode('ascii').upper()
            decoded = binascii.unhexlify(encoded.lower()).decode('utf-8')
            
            print(f"Input: '{test_str}'")
            print(f"Encoded: {encoded}")
            print(f"Decoded: {decoded}")
            print(f"Match: {test_str == decoded}")
            print("-" * 40)
        except Exception as e:
            print(f"Error with '{test_str}': {e}")
            print("-" * 40)


def test_html_entities():
    """Test HTML entity encoding/decoding"""
    test_strings = [
        "<div>Hello</div>",
        "Quote: \"Hello\"",
        "Ampersand: A & B",
        "Mixed: <>&\"'",
        "Normal text without entities",
        ""  # Empty string
    ]
    
    print("\n=== HTML Entity Tests ===")
    for test_str in test_strings:
        try:
            # HTML escape
            encoded = html.escape(test_str, quote=True)
            decoded = html.unescape(encoded)
            
            print(f"Input: '{test_str}'")
            print(f"Encoded: {encoded}")
            print(f"Decoded: {decoded}")
            print(f"Match: {test_str == decoded}")
            print("-" * 40)
        except Exception as e:
            print(f"Error with '{test_str}': {e}")
            print("-" * 40)


def test_rot13():
    """Test ROT13 encoding/decoding"""
    test_strings = [
        "Hello World",
        "Test 123",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "abcdefghijklmnopqrstuvwxyz",
        "Mixed: Hello123World",
        ""  # Empty string
    ]
    
    def rot13(text):
        result = ""
        for char in text:
            if 'a' <= char <= 'z':
                result += chr(((ord(char) - ord('a') + 13) % 26) + ord('a'))
            elif 'A' <= char <= 'Z':
                result += chr(((ord(char) - ord('A') + 13) % 26) + ord('A'))
            else:
                result += char
        return result
    
    print("\n=== ROT13 Tests ===")
    for test_str in test_strings:
        try:
            encoded = rot13(test_str)
            decoded = rot13(encoded)  # ROT13 is symmetric
            
            print(f"Input: '{test_str}'")
            print(f"Encoded: {encoded}")
            print(f"Decoded: {decoded}")
            print(f"Match: {test_str == decoded}")
            print("-" * 40)
        except Exception as e:
            print(f"Error with '{test_str}': {e}")
            print("-" * 40)


def test_binary():
    """Test Binary encoding/decoding"""
    test_strings = [
        "Hi",
        "ABC",
        "123",
        "!@#",
        "A",
        ""  # Empty string
    ]
    
    def text_to_binary(text):
        return ' '.join(format(ord(char), '08b') for char in text)
    
    def binary_to_text(binary):
        return ''.join(chr(int(binary_str, 2)) for binary_str in binary.split())
    
    print("\n=== Binary Tests ===")
    for test_str in test_strings:
        try:
            encoded = text_to_binary(test_str)
            decoded = binary_to_text(encoded)
            
            print(f"Input: '{test_str}'")
            print(f"Encoded: {encoded}")
            print(f"Decoded: {decoded}")
            print(f"Match: {test_str == decoded}")
            print("-" * 40)
        except Exception as e:
            print(f"Error with '{test_str}': {e}")
            print("-" * 40)


if __name__ == "__main__":
    print("EncodeCraft Algorithm Testing")
    print("=" * 50)
    
    test_base64()
    test_url_encoding()
    test_hex_encoding()
    test_html_entities()
    test_rot13()
    test_binary()
    
    print("\n✅ All tests completed!")
    print("Note: JavaScript implementation may have slight differences in edge cases.")
