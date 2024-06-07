
# Terraform Installation

## Windows

### Download Terraform

Go to the [Terraform releases](https://developer.hashicorp.com/terraform/install) page and download the corresponding binary file for Windows.

### Unzip the File

Unzip the downloaded `.zip` file to any directory on your computer.

### Add Terraform to the PATH Environment Variable

To be able to run Terraform from anywhere on the command line, add the directory where you unzipped Terraform to the PATH environment variable:

1. Right-click on **This PC** and select **Properties**.
2. Click **Advanced system settings**.
3. In the **System Properties** window, click **Environment Variables**.
4. In the **System variables** section, find the `Path` variable, select it and click **Edit**.
5. Click **New** and add the path to the directory where the Terraform binary file is located. For example, if you extracted Terraform to `C:\terraform`, add `C:\terraform` to the list.
6. Click **OK** to save the changes and close all windows.

### Check the Installation

Open a new command line window and verify that Terraform is installed correctly by running:

```cmd
terraform -version
```
---

## macOS

### Download Terraform

Go to the [Terraform releases](https://developer.hashicorp.com/terraform/install) page and download the corresponding binary file for macOS.

### Unzip the File

Unzip the downloaded `.zip` file in a terminal:

```sh
unzip terraform_*.zip
```

### Move the Binary File

Move the unzipped binary file to a directory that is in your system path (`PATH`), such as `/usr/local/bin`:

```sh
sudo mv terraform /usr/local/bin/
```

### Check the Installation

Verify that Terraform has been installed correctly:

```sh
terraform -version
```
---

## Linux (Ubuntu/Debian)

```sh
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

---

# Terraform File Configuration

## Terraform Variables

In the `Terraform/terraform.tfvars` file, set the following variables:

```hcl
email_address = "<email>"
log_name      = "<log_name>"
project       = "<project ID>"
```
---

# Executing the Terraform File

In the `Terraform` folder, issue the following commands:

```sh
terraform init
terraform apply
```
---