import os, uuid
from carpartsfinder.helpers import SQL
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from azure.core import credentials

# Retrieve the connection string for use with the application. The storage
# running the application called AZURE_STORAGE_CONNECTION_STRING. If the environment variable is
# created after the application is launched in a console or with Visual Studio,
# the shell or application needs to be closed and reloaded to take the
# environment variable into account.
CONNECT_STR = <ENDPOINT>

# Create a blob client using the local file name as the name for the blob
blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)

# New instance of database
db = SQL("database.db")


def upload(file, id):
    """Uploads a file to Azure Blob Service"""
    blob_client = blob_service_client.get_blob_client(container="partpictures", blob=file.filename)
    tags = {"id":id}
    speed = blob_client.upload_blob(file.stream.read())
    url = blob_client.url
    blob_client.set_blob_tags(tags)
    return url

def delete(name):
    """Deletes a file from Azure Blob Service"""
    blob_client = BlobClient.from_connection_string(CONNECT_STR,"partpictures", name)
    blob_client.delete_blob() 
