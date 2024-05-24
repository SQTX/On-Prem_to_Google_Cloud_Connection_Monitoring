# On-Prem to Google Cloud Connection Monitoring

![Google Cloud](https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)
![Apache](https://img.shields.io/badge/apache-%23D42029.svg?style=for-the-badge&logo=apache&logoColor=white)



## About

On-prem to Google Cloud Connection Monitoring is an open-source monitoring agent. Its purpose is to 
monitor and then resolve any network connectivity issues with Google Cloud resources.

## Installation

### Windows

1. **Install Google Cloud SDK**, a set of tools for managing resources and applications hosted on 
2. Google Cloud. On Windows, it is possible to use the Google Cloud CLI Installer, which is the 
3. easiest way to install Google Cloud SDK.

    1.1 Download and open [Google Cloud CLI Installer](https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe)

    1.2 After opening, it is required to log in to Google

    1.3 Choose the cloud project to use

    1.4 Choose the Default Compute Region and Zone. If the desired zone is not listed, type `list`
   to list all zones.

2. **Create and configure an access key**:

    **Warning**: The limit for the number of keys that can be created for a single service account in Google Cloud is 10 keys.

    2.1 Create an access key on your Google Cloud account, to do this follow the steps listed below:

    - Go to **Administration** -> **Service Accounts**
    - Click on the specific service account
    - Go to the **Keys** tab
    - Click on **Add key**, then create a new key
    - Select JSON key type and click on create
    - The key will be automatically downloaded
    - Activate the service account by running the following command, with the account name and path to the downloaded key file:
    
    ```bash
    gcloud auth activate-service-account SERVICE_ACCOUNT@DOMAIN.COM --key-file=/path/key.json
    ```

    The detailed documentation for this step can be found [here](https://cloud.google.com/sdk/gcloud/reference/auth/activate-service-account).

3. Put the downloaded key in the `/key` folder in the project and change its name to `key.json`.

4. To enable the agent to function properly, it is necessary to fill in several pieces of information in `user-config.yaml`. With these, the application will be able to both connect to the cloud service and control its operation.

5. Install the necessary Python libraries to enable communication with Google Cloud services:
    - numpy
    - smtplib
    - ssl
    - pyyaml
    - python-dotenv
    - mail
    - icmplib
    - google-cloud-monitoring
    - google-cloud-logging

    To do so, open the terminal and execute the following commands:

    ```bash
    pip install numpy
    pip install smtplib
    pip install ssl
    pip install pyyaml
    pip install python-dotenv
    pip install mail
    pip install icmplib
    pip install google-cloud-monitoring
    pip install google-cloud-logging
    ```

## Terraform
You can use Terraform to generate a ready-made Google Cloud project/infrastructure. 
Instructions for use: [Terraform_instruction]()

## Licence Apache License 2.0
More information you can find here: [Apache_License](https://github.com/SQTX/On-Prem_to_Google_Cloud_Connection_Monitoring/blob/main/LICENSE)

---

[//]: # (<p align="center">)
[//]: # (  <img src="https://github.com/SQTX/U2F_arduino_key/blob/main/img/btn+rc.png?">)
[//]: # (</p>)