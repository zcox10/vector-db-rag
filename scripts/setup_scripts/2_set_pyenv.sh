#!/bin/bash

# Prompt for the Python version, default to 3.11.2 if not provided
read -p "Enter the Python version to install (or press Enter to use 3.11.2): " python_version
python_version=${python_version:-3.11.2}

# Install the specified Python version using pyenv
echo -e "\n\n===== Installing Python version $python_version =====\n\n"
pyenv install "$python_version"

# Prompt for the virtual environment name
echo -e "\n"
read -p "Enter a name for the virtual environment: " env_name

# Create the virtual environment
echo -e "\n\n===== Creating virtual environment '$env_name' =====\n\n"
pyenv virtualenv "$python_version" "$env_name"

# Teardown
echo -e "\n\n===== Initiate teardown. Removing unnecessary files  =====\n\n"
rm .wget-hsts
rm setup_scripts/.wget-hsts

# Final message
echo -e "\n\n===== Setup completed successfully! =====\n\n"