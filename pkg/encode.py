import base64

def isEncoded(sb):
    try:
        if isinstance(sb, str):
                # If there's any unicode here, an exception will be thrown and the function will return false
                sb_bytes = bytes(sb, 'ascii')
        elif isinstance(sb, bytes):
                sb_bytes = sb
        else:
                raise ValueError("Argument must be string or bytes")
        return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
    except Exception:
        return False

def encode(api_token):
    token_bytes = api_token.encode('ascii')
    base64_bytes = base64.b64encode(token_bytes)
    base64_token = base64_bytes.decode('ascii')    
    return base64_token

def decode(encoded_api_token):
    base64_bytes = encoded_api_token.encode('ascii')
    token_bytes = base64.b64decode(base64_bytes)
    token = token_bytes.decode('ascii')
    return token