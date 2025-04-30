# secops-detection-as-code

# Detection as Code in Terraform for Google SecOps

This blueprint is a sample terraform repository to implementing a Detection as code pipeline for managing Google SecOps
rules based on Terraform code.
For more information of the code available and how to use it to deploy rules in SecOps please refer to
this [medium article](https://medium.com/p/646de8967278).



### Deployment

#### Step 0: Cloning the repository

If you want to deploy from your Cloud Shell, click on [Cloud Shell] in GCP Console.
Otherwise, in your console of choice:

```bash
git clone https://github.com/ashnaiku/secops-detection-as-code.git
```

Create a Python virtual environment:
```bash
python -m venv ENV_NAME
```

Activate the virtual environment:
# On Linux/macOS:
```bash
source ENV_NAME/bin/activate
```
# On Windows:
```bash
ENV_NAME\Scripts\activate
```
#### Step 1: Upload YARA-L rules to SecOps

   You will need a `<BACKSTORY_CREDENTIALS_FILE>` to run this script. This file can be obtained from the Malachite project.

   **Compare local rules with SecOps rules (dry run):**

   ```bash
   python3 uploadrules.py -c <BACKSTORY_CREDENTIALS_FILE>
   ```

   This command compares the local YARA-L rules with the rules already existing in your SecOps instance. It **does not** upload any files. It is recommended to run this command before actually uploading the rules to identify any potential conflicts or issues.
Before you deploy the architecture, you will need at least the following
information/configurations in place (for more precise configuration see the Variables section):

* A SecOps tenant deployed with BYOP
* The SecOps project ID
* Region and customer code for the SecOps tenant
* Chronicle API Admin or equivalent to access SecOps APIs
* Cloud Storage bucket for storing remote state file

#### Step 2: Prepare the variables for Terraform

Once you have the required information, head back to your cloned repository.
Make sure you’re in the directory of this tutorial (where this README is in).

Configure the Terraform variables in your `terraform.tfvars` file.
Rename the existing `terrafomr.tfvars.sample` as starting pointand then see the variables
documentation below.

For the pipeline to work properly it is mandatory to keep the terraform state in a remote location.
We recommend a Cloud Storage bucket for storing the state file, we provided a sample backend.tf file
named `backend.tf.sample` you can rename to backend.tf and replace the name of the Cloud Storage bucket where to store
state file. It is important for the accoung running the terraform script to have access to such a Cloud Storage bucket.

#### Step 3: Deploy resources

Initialize your Terraform environment and deploy the resources:

```shell
terraform init
terraform apply
```

<!-- BEGIN TFDOC -->

## Variables

| name                                      | description                                                            |                                                                                                      type                                                                                                      | required |                                                                                  default                                                                                   |
|-------------------------------------------|------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:--------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| [secops_tenant_config](variables.tf#L29)  | SecOps tenant configuration.                                           | <code title="object&#40;&#123;&#10;  location &#61; optional&#40;string, &#34;eu&#34;&#41;&#10;  instance &#61; string&#10;  project  &#61; string&#10;&#125;&#41;">object&#40;&#123;&#8230;&#125;&#41;</code> |    ✓     |                                                                                                                                                                            |
| [secops_content_config](variables.tf#L17) | Path to SecOps rules and reference lists deployment YAML config files. |                             <code title="object&#40;&#123;&#10;  reference_lists &#61; string&#10;  rules &#61; string&#10;&#125;&#41;">object&#40;&#123;&#8230;&#125;&#41;</code>                             |          | <code title="&#123;&#10;  reference_lists &#61; &#34;secops_reference_lists.yaml&#34;&#10;  rules &#61; &#34;secops_rules.yaml&#34;&#10;&#125;">&#123;&#8230;&#125;</code> |

<!-- END TFDOC -->

## Test

```hcl
module "test" {
  source        = "./fabric/blueprints/secops/detection-as-code"
  secops_config = {
    location = "eu"
    instance = "XXXXXX-XXX-XXXXXX"
    project  = "secops-project"
  }
}
# tftest modules=1 resources=2 files=rule,config
```

```
# tftest-file id=rule path=rules/network_traffic_to_specific_country.yaral
rule network_traffic_to_specific_country {

  meta:
    author = "Google Cloud Security"
    description = "Identify network traffic based on target country"
    type = "alert"
    tags = "geoip enrichment"
    data_source = "microsoft windows events"
    severity = "Low"
    priority = "Low"

  events:
    $network.metadata.event_type = "NETWORK_CONNECTION"
    //Specify a country of interest to monitor or add additional countries using an or statement
    $network.target.ip_geo_artifact.location.country_or_region = "France" nocase
    $network.target.ip = $ip

  match:
    $ip over 30m

  outcome:
    $risk_score = max(35)
    $event_count = count_distinct($network.metadata.id)

    // added to populate alert graph with additional context
    $principal_ip = array_distinct($network.principal.ip)

    // Commented out target.ip because it is already represented in graph as match variable. If match changes, can uncomment to add to results
    //$target_ip = array_distinct($network.target.ip)
    $principal_process_pid = array_distinct($network.principal.process.pid)
    $principal_process_command_line = array_distinct($network.principal.process.command_line)
    $principal_process_file_sha256 = array_distinct($network.principal.process.file.sha256)
    $principal_process_file_full_path = array_distinct($network.principal.process.file.full_path)
    $principal_process_product_specfic_process_id = array_distinct($network.principal.process.product_specific_process_id)
    $principal_process_parent_process_product_specfic_process_id = array_distinct($network.principal.process.parent_process.product_specific_process_id)
    $target_process_pid = array_distinct($network.target.process.pid)
    $target_process_command_line = array_distinct($network.target.process.command_line)
    $target_process_file_sha256 = array_distinct($network.target.process.file.sha256)
    $target_process_file_full_path = array_distinct($network.target.process.file.full_path)
    $target_process_product_specfic_process_id = array_distinct($network.target.process.product_specific_process_id)
    $target_process_parent_process_product_specfic_process_id = array_distinct($network.target.process.parent_process.product_specific_process_id)
    $principal_user_userid = array_distinct($network.principal.user.userid)
    $target_user_userid = array_distinct($network.target.user.userid)

  condition:
    $network
}
```

```
# tftest-file id=config path=secops_rules.yaml
network_traffic_to_specific_country:
  enabled: true
  alerting: true
  archived: false
  run_frequency: "DAILY"
```
