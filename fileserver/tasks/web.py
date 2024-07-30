from celery import shared_task

# Read in 1 MB chunks
CHUNKSIZE=1024 * 1024

@shared_task
def process_uploaded_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(CHUNKSIZE)
                if not chunk:
                    break
                # Process the chunk here
                # For example, you might parse data and save it to the database
    except Exception as e:
        # Handle any exceptions that occur during file processing
        print(f'Error processing file {file_path}: {e}')