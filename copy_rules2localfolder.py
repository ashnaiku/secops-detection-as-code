import os
import shutil
import yaml
from git import Repo

def clone_and_copy():
  """Clones the detection-rules repository and copies .yaral files to a local directory."""

  # Define the source and destination directories
  repo_url = "https://github.com/chronicle/detection-rules"
  local_dir = "rules"
  tf_rules_folder = "newrules" # Define the tf_rules_folder variable
  # Clone the repository
  try:
    Repo.clone_from(repo_url, local_dir)
    print(f"Successfully cloned repository to {local_dir}")
  except Exception as e:
    print(f"Error cloning repository: {e}")
    return

  # -----------------
  # Walk through the cloned repository and copy .yaral files
  for root, _, files in os.walk(local_dir):
    for file in files:
      if file.endswith((".yaral", ".yara")):
        source_path = os.path.join(root, file)
        destination_path = os.path.join(local_dir, file)
        try:
          shutil.move(source_path, destination_path)
          # print(f"Copied {file} to {local_dir}")
        except Exception as e:
          print(f"Error copying {file}: {e}")
  print(f"Copied all file to {local_dir}")          
  

  manage_yaral_files_and_folders(tf_rules_folder, local_dir)

  process_yara_rules(rules_folder=local_dir, output_file="secops_rules.yaml")
# -------------------------------------

# -------------------------------------- 
def manage_yaral_files_and_folders(tf_rules_folder, local_dir):
    """
    Moves .yaral files from the tf_rules_folder to the local_dir and
    interactively deletes empty folders within the local_dir.

    Args:
        tf_rules_folder (str): The path to the folder containing .yaral files to move.
        local_dir (str): The local directory to move the files to and to check for empty folders.
    """
    
    # Store the original working directory
    original_dir = os.getcwd()
    
    # Move .yaral files from tf_rules_folder to local_dir
    for filename in os.listdir(tf_rules_folder):
        if filename.endswith(".yaral"):
            source_path = os.path.join(tf_rules_folder, filename)
            destination_path = os.path.join(local_dir, filename)
            try:
                shutil.move(source_path, destination_path)
                print(f"Moved '{filename}' from '{tf_rules_folder}' to '{local_dir}'")
            except Exception as e:
                print(f"Error moving '{filename}' from '{tf_rules_folder}' to '{local_dir}': {e}")

    # Change to the specified directory
    try:
        os.chdir(local_dir)
        print(f"Changed current directory to: {local_dir}")
    except FileNotFoundError:
        print(f"Error: Directory '{local_dir}' not found.")
        return
    except NotADirectoryError:
        print(f"Error: '{local_dir}' is not a valid directory.")
        return

    # Ask for confirmation before deleting empty folders
    confirmation = input(f"Are you sure you want to delete all folders in '{local_dir}'? (y/n): ")
    if confirmation.lower() != 'y':
        print("Deletion of folders cancelled.")
        # Change back to the original directory
        os.chdir(original_dir)        
        return

    for item in os.listdir():
        item_path = os.path.join(local_dir, item)
        # Check if the item is a directory
        if os.path.isdir(item_path):
            try:
                # Try to remove the directory; it will fail if not empty
                os.rmdir(item_path)
                print(f"Deleted empty folder: '{item}'")
            except OSError:
                # If OSError occurs, the directory is not empty, so skip
                print(f"Skipping non-empty folder: '{item}'")
            except Exception as e:
                print(f"Error deleting folder '{item}': {e}")
    
    # Change back to the original directory
    os.chdir(original_dir)
    print(f"Changed back to the original directory: {original_dir}")                
# -------------------------------------

def process_yara_rules(rules_folder="rules", output_file="secops_rules.yaml"):
    """
    1. Lists all .yaral files in the specified folder.
    2. Creates a list of dictionaries, where each dictionary contains the
       filename (without the .yaral extension) as the key.
    3. Deletes or overwrites the 'secops_rules.yaml' file if it exists.
    4. Creates a new 'secops_rules.yaml' file and populates it with rule
       configurations based on the found .yaral files.
    """
    list_yarafiles = []
    if os.path.exists(rules_folder) and os.path.isdir(rules_folder):
        for filename in os.listdir(rules_folder):
            if filename.endswith(".yaral"):
                rule_name = filename[:-6]  # Remove the ".yaral" extension
                # print(f"rule_name 3: {rule_name}")
                list_yarafiles.append({rule_name: None}) # Append a dictionary

    # Delete or overwrite secops_rules.yaml
    if os.path.exists(output_file):
        try:
            os.remove(output_file)
            print(f"Deleted existing '{output_file}'")
        except OSError as e:
            print(f"Error deleting '{output_file}': {e}")
            return
    print(f"Progress so far ...  '{output_file}' and rules_folder:{rules_folder}")
    # Open and write to the new secops_rules.yaml
    try:
        with open(output_file, 'w') as yaml_file:
            rules_config = {}
            print(f"opened file ... ")
            for item in list_yarafiles:
                for rule_name in item.keys():
                    print(f"rule_name: {rule_name}")
                    rules_config[rule_name] = {
                        "enabled": True,
                        "alerting": True,
                        "archived": False,
                        "run_frequency": "DAILY"
                    }
            yaml.dump(rules_config, yaml_file, sort_keys=False)
        print(f"Successfully created '{output_file}' with rules from '{rules_folder}'.")

    except IOError as e:
        print(f"Error writing to '{output_file}': {e}")
    except yaml.YAMLError as e:
        print(f"Error during YAML serialization: {e}")


# -------------------------------------
if __name__ == "__main__":
  clone_and_copy()
# Example usage
  # source_directory = '.'  # Current folder
  # destination_directory = '/Users/ashnaiku/Downloads/Samples/ChronicleSamples/upload_rules/localRules'
  
