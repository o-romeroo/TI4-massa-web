import base64
from typing import Optional


@staticmethod
def blob_to_base64(blob_data: Optional[bytes]) -> Optional[str]:
    if blob_data is None:
        return None

    try:
        base64_string = base64.b64encode(blob_data).decode('utf-8')
        return base64_string
    except Exception as e:
        print(f"Error encoding BLOB to Base64: {e}")
        return None