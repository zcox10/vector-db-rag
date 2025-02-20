# Setup Scripts Documentation

This repository contains two Bash scripts designed to streamline the setup of a development environment. These scripts automate the installation of essential tools, configure Python environments, and facilitate secure access to GitHub repositories.

---

## **1. Installation Script: `1_installations.sh`**

### **Overview**
This script performs system updates, installs necessary dependencies, configures GitHub SSH access, and installs `pyenv` for Python version management. Make the scripts executable by running:
```bash
chmod +x 1_installations.sh 2_set_pyenv.sh
```

### **Key Steps:**
1. **System Update:**
   - Updates and upgrades system packages.

2. **Dependency Installation:**
   - Installs essential development tools, including:
     - `gcc`, `tmux`, `git`, `make`, `build-essential`
     - Libraries for Python and system compatibility (`libssl-dev`, `zlib1g-dev`, `libbz2-dev`, etc.)

3. **GCC Verification:**
   - Checks if `gcc` is successfully installed.

4. **GitHub SSH Key Configuration:**
   - Prompts for GitHub email and username.
   - Generates an SSH key for secure GitHub access if it doesn't already exist.
   - Configures the SSH client for GitHub access.
   - Adds the SSH key to the SSH agent.

5. **GitHub Repository Cloning:**
   - Prompts for a GitHub repository URL (default: `vector-db-rag`).
   - Creates a user-specific directory and clones the repository if it doesn't exist.

6. **Git Configuration:**
   - Sets the local Git user email and name for the repository.

7. **Pyenv Installation:**
   - Installs `pyenv` and configures it in `.bashrc`.

8. **Final Instructions:**
   - Prompts to restart the shell or run `exec $SHELL` for changes to take effect.


## **2. Python Environment Setup Script: `2_set_pyenv.sh`**

### **Overview**
This script configures the Python environment using `pyenv` by installing a specific Python version and creating a virtual environment.

### **Key Steps:**
1. **Python Version Installation:**
   - Prompts for the desired Python version (default: `3.11.2`).
   - Installs the specified version using `pyenv`.

2. **Virtual Environment Creation:**
   - Prompts for the virtual environment name.
   - Creates a virtual environment associated with the specified Python version.

3. **Teardown:**
   - Removes temporary setup files (e.g., `.wget-hsts`).

4. **Completion Message:**
   - Confirms successful setup.

## **Usage Instructions**

### **Step 1: Run the Installation Script**
```bash
bash 1_installations.sh
```
- Follow the prompts to enter your GitHub email, username, and repository URL.
- Ensure you add the generated SSH key to your GitHub account.
- Restart your shell after installation.

### **Step 2: Run the Python Environment Setup Script**
```bash
bash 2_set_pyenv.sh
```
- Enter the desired Python version (or press Enter for the default `3.11.2`).
- Specify a name for the virtual environment.