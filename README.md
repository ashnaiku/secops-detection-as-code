
# Detection as Code in Terraform for Google SecOps

This blueprint is a sample terraform repository to implementing a Detection as code pipeline for managing Google SecOps
rules based on Terraform code.
For more information of the code available and how to use it to deploy rules in SecOps please refer to
this [medium article](https://medium.com/p/646de8967278).



## Prerequisites

* Python 3.6 or later

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ashnaiku/secops-detection-as-code.git
   ```

2. **Create a Python virtual environment:**

   ```bash
   python -m venv <ENV_NAME>
   ```

3. **Activate the virtual environment:**

   ```bash
   # On Linux/macOS:
   source <ENV_NAME>/bin/activate

   # On Windows:
   <ENV_NAME>\Scripts\activate
   ```

4. **Install the required Python libraries:**

   ```bash
   pip install -r requirements.txt
   ```


## Usage

#### Step 1: Copy YARA-L rules to a local folder:

   ```bash
   python3 copy_rules2localfolder.py
   ....
   Are you sure you want to delete empty folders in localtmp? (y/n): y
   ....
   ls localtmp/
   ```

   This script copies all YARA-L rule files from the [chronicle/detection-rules](https://github.com/chronicle/detection-rules.git) repository to a local folder named `localtmp`. This repository houses a collection of pre-built YARA rules.

#### Step 2: Prepare the variables for Terraform
Before you deploy the architecture, you will need at least the following
information/configurations in place :

#### Step 2a - Variables
Configure the Terraform variables in your `terraform.tfvars` file.
Rename the existing `terrafomr.tfvars.sample` as starting pointand then see the variables
documentation below.
* Region and customer code for the SecOps instance
* Customer ID of SecOps instance (deployed with BYOP) 
* The SecOps BYOP project ID
* Chronicle API Admin or equivalent to access SecOps APIs


```bash
   mv terraform.tfvars.sample terraform.tfvars
```

#### Step 2b - Cloud Storage bucke
For the pipeline to work properly it is mandatory to keep the terraform state in a remote location.
We recommend a Cloud Storage bucket for storing the state file, we provided a sample backend.tf file
named `backend.tf.sample` you can rename to `backend.tf` and replace the name of the Cloud Storage bucket where to store
state file. It is important for the accoung running the terraform script to have access to such a Cloud Storage bucket.

* Cloud Storage bucket for storing remote state file

```bash
   mv backend.tf.sample	backend.tf
```
  
#### Step 3: Deploy resources

Initialize your Terraform environment and deploy the resources:

```shell
terraform init
terraform apply
```


## Test

```hcl
module "test" {
  source        = "./fabric/blueprints/secops/detection-as-code"
  secops_config = {
    location = "us"
    instance = "XXXXXX-XXX-XXXXXX"
    project  = "XXX-secops-project"
  }
}
# tftest modules=1 resources=2 files=rule,config
```

