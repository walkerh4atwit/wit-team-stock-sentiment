from oci.response import Response
import oci
import os
import base64
from zipfile import ZipFile

def stream_file(fname: str, http_response: Response):
    with open(fname, 'wb') as file:
        for chunk in http_response.data.raw.stream(1024 * 1024, decode_content=False):
            file.write(chunk)

# this function signs into oci and copies in the db wallet
def oci_util():
    key_bytes: bytes = base64.b64decode(os.environ.get("OCI_CLI_KEY_CONTENT"))
    key_content = key_bytes.decode()

    config = {
        "user": os.environ.get("OCI_CLI_USER"),
        "fingerprint": os.environ.get("OCI_CLI_FINGERPRINT"),
        "key_content": key_content,
        "tenancy": os.environ.get("OCI_CLI_TENANCY"),
        "region": os.environ.get("OCI_CLI_REGION")
    }

    client = oci.object_storage.ObjectStorageClient(config)

    response: Response = client.get_namespace()
    namespace = response.data
    bucket_name = 'sentiments-llm-bucket'
    object_name = 'Wallet-' + os.environ.get("BUILD_ENV") + '.zip'

    response = client.get_object(
        namespace,bucket_name,object_name        
    )

    stream_file(response, object_name)

    wallet = ZipFile(object_name, 'r')
    wallet.extractall()