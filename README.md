# On-Prem_to_Google_Cloud_Connection_Monitoring


# WINDOWS

## About

On-prem to Google Cloud Connection Monitoring is an open-source monitoring agent. Its purpose is to monitor and then resolve any network connectivity issues with Google Cloud resources.

## Installation

1. **Install Google Cloud SDK**, a set of tools for managing resources and applications hosted on Google Cloud. On Windows, it is possible to use the Google Cloud CLI Installer, which is the easiest way to install Google Cloud SDK.

    1.1 Download and open [Google Cloud CLI Installer](https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe)

    1.2 After opening, it is required to log in to Google

    1.3 Choose the cloud project to use

    1.4 Choose the Default Compute Region and Zone. If the desired zone is not listed, type `list` to list all zones.

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

    - os
    - numpy
    - smtplib
    - ssl
    - time
    - pyyaml
    - python-dotenv
    - mail
    - icmplib
    - google-cloud-monitoring
    - google-cloud-logging

    To do so, open the terminal and execute the following commands:

    ```bash
    pip install os
    pip install numpy
    pip install smtplib
    pip install ssl
    pip install time
    pip install pyyaml
    pip install python-dotenv
    pip install mail
    pip install icmplib
    pip install google-cloud-monitoring
    pip install google-cloud-logging
    ```
```
