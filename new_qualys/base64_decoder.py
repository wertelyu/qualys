import base64


def decode_64(base64_message):
    """
    На входе функция получает закодированную строку.
    return: decoding string
    """
    try:
        base64_bytes = base64_message.encode('utf-8')
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode('utf-8')
        return message
    except UnicodeDecodeError as e:
        print(e)


if __name__ == '__main__':
    print(decode_64(""""++0YLQvtCyIERPTSwg0LLRi9C/0L7Qu9C90Y/QtdC8INC40L3QuNGG0LjQsNC70Lj
                    Qt9Cw0YbQuNGOCgl5bWFwcy5yZWFkeShpbml0KTsKCglmdW5jdGlvbiBpbml0ICgpIHs
                    KCQl2YXIgbXlNYXAgPSBuZXcgeW1hcHMuTWFwKCJtYXAyIiwgewoJCQkJY2VudGVyOiBb
                    OQo7KGZ1bmN0aW9uKCl7cXhzc30pOy8vLCAzNy41NzE4MzMxMDE4NTJdLAoJCQkJem9vbT
                    ogMTYKCQkJfSksCgkJCS8vINCf0LXRgNCy0YvQuSDRgdC/0L7RgdC+0LEg0LfQsNC00LDQv
                    dC40Y8g0LzQtdGC0LrQuAoJCQlteVBsYWNlbWFyayA9IG5ldyB5bWFwcy5QbGFjZW1hcmsoW
                    zkKOyhmdW5jdGlvbigpe3F4c3N9KTsvLywgMzcuNTcxODMzMTAxODUyXSk7CgkJCgkJbXlNY
                    XAuY29udHJvbHMuYWRkKCd6b29tQ29udHJvbCcpLmFkZCgnbWFwVG9vbHMnKTsKCgkJLy8g0
                    JTQvtCx0LDQstC70Y/QtdC8IA==="""))
