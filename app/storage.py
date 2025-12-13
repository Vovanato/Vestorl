import os
import uuid
from azure.storage.blob import BlobServiceClient
def upload_file(file,filename):
    ext=filename.rsplit('.',1)[1]
    unique_id=(uuid.uuid4())
    new_filename=f"{unique_id}.{ext}"
    conn_str=os.getenv('AZURE_CONNECTION_STRING')
    service_client=BlobServiceClient.from_connection_string(conn_str) 
    blob_client=service_client.get_blob_client(container="uploads",blob=new_filename)
    blob_client.upload_blob(file)
    return blob_client.url, new_filename
def delete_file(filename):
    conn_str=os.getenv('AZURE_CONNECTION_STRING')
    service_client=BlobServiceClient.from_connection_string(conn_str) 
    blob_client=service_client.get_blob_client(container="uploads",blob=filename)
    blob_client.delete_blob()