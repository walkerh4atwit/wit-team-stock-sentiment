from oci.response import Response
import oci
import os
import base64
from zipfile import ZipFile

# this function signs into oci and copies in the db wallet
def oci_util():
    key_bytes: bytes = base64.b64decode(os.environ.get("OCI_CLI_KEY_CONTENT"))
    key_content = key_bytes.decode()

    client = oci.object_storage.ObjectStorageClient(
        {
            "name": os.environ.get("OCI_CLI_USER"),
            "fingerprint": os.environ.get("OCI_CLI_FINGERPRINT"),
            "key_content": key_content,
            "tenancy": os.environ.get("OCI_CLI_TENANCY"),
            "region": os.environ.get("OCI_CLI_REGION")
        }
    )

    response: Response = client.get_namespace()
    namespace = response.data
    bucket_name = 'sentiments-llm-bucket'
    object_name = 'Wallet-' + os.environ.get("BUILD_ENV")

    response = client.get_object(
        namespace,bucket_name,object_name        
    )

    with open('Database-Wallet', 'wb') as file:
        file.write(response.data)

    wallet = ZipFile(object_name, 'r')
    wallet.extractall()