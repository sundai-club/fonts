import os
import argparse

import subprocess
import zipfile
import webbrowser
import os



def user_model():
    """
    Prompt the user to input the fine tune model name
    """
    does_model_exist = input("Have you already created the model on Replicate? (y/n): ")

    if does_model_exist.lower() == "y":
        model_name = input("Please input the model name (owner/model_name): ")
        return model_name
    else:
        name = input("What do you want to call the model? Pick a short and memorable name. Use lowercase characters and dashes. (eg: sdxl-barbie, musicgen-ye): ")
        webbrowser.open(f"https://replicate.com/create?name={name}")
        input("Once you have created the model (click Create on the webpage that just opened), press Enter to continue.")
        owner = input("What is your Replicate username? ")
        return f"{owner}/{name}"


def zip_directory(folder_path, zip_path):
    """
    Compress a directory (with all files in it) into a zip file.

    :param folder_path: Path of the folder you want to compress.
    :param zip_path: Destination file path, including the filename of the new zip file.
    """
    print(f"Zipping {folder_path} to {zip_path} ...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

    return zip_path

def replicate_train(model, save_dir, replicate_repo, caption_prefix="in the style of TOK"):
    try:
        # Please make sure that 'replicate' is installed and available in your system's PATH.
        command = [
            "replicate",
            "train",
            replicate_repo,
            "--destination",
            model,
            "--web",
            f"input_images=@{save_dir}",
            f"caption_prefix={caption_prefix}",
        ]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("Error executing the command:", str(e))
    except FileNotFoundError:
        print("Error: 'replicate' command not found. Is it installed correctly?")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def is_replicate_api_token_set():
    return 'REPLICATE_API_TOKEN' in os.environ

def is_replicate_cli_installed():
    try:
        subprocess.check_output(["replicate", "--version"])
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False


def check_repo(replicate_repo):
    # TODO 
    # check that replicate repo exists 
    
    
    
    return replicate_repo
    
    
    
def create_training(args):
    # If the user confirms, proceed with the posting function
    model = user_model()
    
    replicate_repo = check_repo(args.replicate_repo)

    # Compress the directory with the images
    if args.input.endswith(".zip"):
        zip_path = args.input
    else: 
        if args.input.endswith("/"):
            args.input = args.input[:-1]
        zip_path = zip_directory(args.input,args.input + ".zip" )

    replicate_train(model, zip_path, replicate_repo, caption_prefix=args.caption_prefix)
    
def main():
    parser = argparse.ArgumentParser(description='Parse image folder')
    parser.add_argument('input', default="images", help='input can be a folder with images or a zip file')
    parser.add_argument('replicate_repo', default="stability-ai/sdxl", help='repository to replicate')
    parser.add_argument('--caption_prefix', default="in the style of TOK", help='tag to use with the trained model')
    args = parser.parse_args()

    if not is_replicate_cli_installed():
        input("🚫 Replicate CLI is not installed. Please install it before proceeding. Link: https://github.com/replicate/cli. Press any key to open the webpage.")
        webbrowser.open(f"https://github.com/replicate/cli")
    else:
        print("✅ Replicate CLI is installed. Proceeding...")

    if not is_replicate_api_token_set():
        print("🚫 REPLICATE_API_TOKEN is not set. Please set it with `export REPLICATE_API_TOKEN=<your-token>`, then try again.")
        return
    else:
        print("✅ REPLICATE_API_TOKEN is set. Proceeding...")

    assert os.path.exists(args.input)

    create_training(args)


if __name__ == "__main__":
    main()
