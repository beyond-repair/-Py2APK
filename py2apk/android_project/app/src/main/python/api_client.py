from java import jclass

def get_api_key():
    APIKeyManager = jclass("com.example.py2apk.APIKeyManager")
    return APIKeyManager.getApiKey()
