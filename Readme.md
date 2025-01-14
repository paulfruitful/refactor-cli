## refactor-cli

**A command-line tool to watch and refactor code using AI.**

refactor-cli is a command-line interface (CLI) tool designed to automate the process of refactoring codes and keeping your codebase clean and error free.
 It provides two main features:

- Watch a directory: Monitors a specified directory for changes in Code files and triggers automatic refactoring when its done watchinh.
- Refactor a single file: Allows users to refactor an individual Code file immediately by providing its full path.

The tool uses AI-powered refactoring to improve code quality and structure, making it more efficient and maintainable.
## Installation (Windows)


**1. Use the Installer:**

  - Locate the `refactor-cli` directory after cloning the repository.
  - Check for a file named `Refactor-cLi-Installer.exe`.
  - Double-click the installer and follow the on-screen instructions.

2.  **Set up Google API Key:**

      - **Obtain an API Key:**
          - Visit [https://console.cloud.google.com/](https://www.google.com/url?sa=E&source=gmail&q=https://console.cloud.google.com/) and create or select a project.
          - Enable Google AI Platform APIs.
          - Create an API key under "Credentials".
      - **Set the environment variable:**
          - Right-click "This PC" or "My Computer" and select "Properties".
          - Go to "Advanced system settings" -\> "Environment Variables".
          - Under "System variables", click "New".
          - Set the "Variable name" to `GOOGLE_API_KEY` and "Variable value" to your API key.
          - Click "OK" on all windows to save changes.

**Verification (open a new command prompt window):**

```bash
python -c "import os; print(os.environ.get('GOOGLE_API_KEY'))"
```
# refactor-cli

This should print your API key if it's set correctly.

## Usage

1. **Watch a directory:**

```bash
refactor-cli watch 
```
Run it in the directory you want to change 

Refactor a single file immediately:
```bash
refactor-cli touch <path_to_file>
```
Replace <path_to_file> with the full path to the Python file you want to refactor.

Installation (Linux)
1. Download the refactor-cli executable:

Obtain the refactor-cli executable file (usually refactor-cli) from the release page of the project repository.
2. Install the executable:

- Open a terminal as root or using sudo :

```bash
sudo su
```
 
- Move the refactor-cli executable to the /usr/local/bin directory:

```bash
mv refactor-cli /usr/local/bin/refactor-cli
```
- Make the executable file executable:

```bash
chmod +x /usr/local/bin/refactor-cli
```
3. **Set up Google API Key:**
- Obtain an API Key:
          - Visit [https://console.cloud.google.com/](https://www.google.com/url?sa=E&source=gmail&q=https://console.cloud.google.com/) and create or select a project.
          - Enable Google AI Platform APIs.
          - Create an API key under "Credentials".
- Set the environment variable:
Create a file named ```google_api_key.sh``` in your home directory (~/):

```bash
export GOOGLE_API_KEY="your_api_key_here"
```
Replace "your_api_key_here" with the actual API key.

- Make the file executable:

```bash
chmod +x ~/google_api_key.sh
```
- Add the following line to your .bashrc or .zshrc file:

```bash
source ~/google_api_key.sh
```
Log out and log back in, or source the file using:

```bash
source ~/.bashrc 
Verification:
```
```bash
refactor-cli --help 
```
This should display the command-line help information if the installation was successful.

## Contributing
We welcome contributions! Please follow these steps:

- Fork the repository.
- Create a new branch for your feature or bug fix.
- Make your changes and commit them with clear messages.
- Push your branch to your fork.
- Create a pull request to the main repository.
## License
This project is licensed under the MIT License.

## Additional Notes
Replace placeholders like  <path_to_file> with actual paths on your system.
An active internet connection is required for the Google AI integration to function.
