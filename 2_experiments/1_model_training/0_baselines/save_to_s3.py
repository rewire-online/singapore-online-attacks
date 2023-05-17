import os
import boto3
import argparse

parser = argparse.ArgumentParser(description='Saves Model Files to s3')
parser.add_argument('-n','--model_name', help='Model Name', required=True)
parser.add_argument('-f','--model_folder', help='Model Folder', required=True)

def main(model_name, model_folder):

    s3 = boto3.resource("s3")
    local_save_path = f"{model_folder}"
    print(f"Saving contents of {local_save_path} to s3")
    for obj in os.listdir(local_save_path):
        print(f"uploading {obj} to s3")
        s3.meta.client.upload_file(
            os.path.join(
                local_save_path,
                obj,
            ),
            'rewire-artifacts-storage',
            os.path.join(
                model_name,
                obj,
            ),
        )
    print(f"Model files saved to s3 folder rewire-artifacts-storage/{model_name}")

if __name__ == "__main__":
    args = vars(parser.parse_args())
    main(args['model_name'], args['model_folder'])