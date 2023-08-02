# CurlGoogle
[![PyPI](https://img.shields.io/pypi/v/curlgoogle.svg?color=green)](https://pypi.org/project/curlgoogle/)

CurlGoogle is a lightweight, easy-to-use, and extremely simple library that allows you to link devices to Google accounts and transfer files (upload/download) using nothing more than the command line. Built on the principles demonstrated in [this article](https://towardsdatascience.com/uploading-files-to-google-drive-directly-from-the-terminal-using-curl-2b89db28bb06), this library offers a lean alternative to more extensive libraries such as [google-drive](https://pypi.org/project/google-drive/). 

With absolutely no specific dependencies needed apart from curl, you can get up and running with file transfers on Google Drive in no time. The library's minimalistic design makes it not only easy to install but also to understand and use.

## Installation
To install the library, open your terminal and type the following command:

```bash
pip install curlgoogle
```
This command installs the library from the source directory (TODO: add to PyPI).

## Usage

(Disclaimer: Most of the explanation here is derived from [this article](https://towardsdatascience.com/uploading-files-to-google-drive-directly-from-the-terminal-using-curl-2b89db28bb06).)

### Installing curl

You should install curl on the device you are trying to run this package (this is the only dependency).
```bash
sudo apt install curl # Linux Debian/Ubuntu
brew install curl # Mac
```
### Creating a Google Cloud Platform Project and Acquiring Credentials
In order to manage access to our Google Drive, we need to establish a level of control. This can be achieved by creating a project that incorporates user-specified permissions. This project will function as an intermediary between our users (or us, when using a different machine) and our Google account. The initial step in this process is to navigate to the [specified page](https://console.developers.google.com/apis/credentials?pli=1) and set up a new project.

Now, select the **Credentials** tab and then create credentials which is **OAuth Client ID** in particular. For app type, you may select anything! 

After setting up, you now have a client ID and a client secret. You will need these to authenticate your requests. To automate the process, we use [Dotenv] to store your secrets. Make sure to add `.env` in your `.gitignore` file to avoid sharing your secrets with the world!

Run the following commands to install dotenv and create a `.env` file with the appropriate variables:

```bash
pip install python-dotenv
dotenv set GDRIVE_CLIENT_ID <your_client_id>
dotenv set GDRIVE_CLIENT_SECRET <your_client_secret>
```

### Upload and Download

After the setup phase, you're good to go! You do not need to repeat this phase again for your project as the credentials are safely stored in your `.env` file and the library automatically loads them when you import it.

You can use either a commandline interface (CLI) to upload/download files, or use the library sdk. 

**important node**: You should extract the file or folder identifiers from their corresponding link.

#### CLI

Use the following format for download and upload
```bash
curlgoogle_upload <file/folder-1> <file/folder-2> ... <file/folder-N> (optional)<folder_id>
```
This will upload all your files or folders into a folder with the specified identifier.

You can also pick a bunch of folders or files, zip them into a single file with a specific name and then upload them all at once using the following convention:

```bash
curlgoogle_upload <file/folder-1> <file/folder-2> ... <file/folder-N> (optional)<folder_id> -m -n <zip_file_name>
```

For download use the following format:
```bash
curlgoogle_download <file_id1> <file_id2> ... <file_idN>
```
This will automatically download the files and extract them.

### SDK

You can also use the following functions for upload and download while development. Note that this will automatically prompt you to authenticate your Google account mid-run; therefore, it might not be the ideal use case for production.

```python
# Uplaoding function
curlgoogle.upload(
    file_name: str, 
    file_list: List[str], 
    folder_id: Optional[str] = None
)
# Downloading function
curlgoogle.download(
    file_id: str
)
```

## License
This project is licensed under [MIT License](./LICENSE).
