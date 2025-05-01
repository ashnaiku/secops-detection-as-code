import os
import shutil

from git import Repo

def clone_and_copy():
  """Clones the detection-rules repository and copies .yaral files to a local directory."""

  # Define the source and destination directories
  repo_url = "https://github.com/chronicle/detection-rules"
  local_dir = "localtmp"
#TODO change to rules
  #TODO Add all rule names secops_rules.yaml 
  # Clone the repository
  try:
    Repo.clone_from(repo_url, local_dir)
    print(f"Successfully cloned repository to {local_dir}")
  except Exception as e:
    print(f"Error cloning repository: {e}")
    return

  # Create the destination directory if it doesn't exist
  os.makedirs(local_dir, exist_ok=True)

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
  
  # Change to the specified directory
  os.chdir(local_dir) 
   # Ask for confirmation
  confirmation = input(f"Are you sure you want to delete empty folders in {local_dir}? (y/n): ")
  if confirmation.lower() != 'y':
    print("Deletion cancelled.")
    return

  for item in os.listdir():
    # Check if the item is a directory and if it's empty
    # if os.path.isdir(item) and not os.listdir(item):
    if os.path.isdir(item):
      print(f"Deleting: {item}")
      shutil.rmtree(item)
# -------------------------------------

# -------------------------------------
if __name__ == "__main__":
  clone_and_copy()
# Example usage
  source_directory = '.'  # Current folder
  destination_directory = '/Users/ashnaiku/Downloads/Samples/ChronicleSamples/upload_rules/localRules'
  
