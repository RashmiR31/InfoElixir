from google.cloud import storage

def upload_blob(file_path, destination_blob_name):
    bucket_name="infoelixir_data"
    # Initialize a storage client
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.bucket(bucket_name)
    # Create a new blob and upload the file's content
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)

    print(f"File {file_path} uploaded to {destination_blob_name}.")

def download_file(bucket_name, source_blob_name, destination_file_name):
    # Initialize a storage client
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.bucket(bucket_name)

    # Get the blob
    blob = bucket.blob(source_blob_name)

    # Download the file to a local path
    blob.download_to_filename(destination_file_name)

    print(f"Downloaded storage object {source_blob_name} from bucket {bucket_name} to local file {destination_file_name}.")

# Usage
# download_file("infoelixir_data", "rashmi/assignment.pdf", "/Users/rashmir/Desktop/hack/file.pdf")

# upload_blob(file_path="/Users/rashmir/Desktop/hack/doc.txt", destination_blob_name="rashmi/document.txt")