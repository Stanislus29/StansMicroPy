# GUIDE FOR INSTALLING MEDIA_PIPE AND IT'S DEPENDENCIES

Author: Somtochukwu Emeka-Onwuneme
---

This guide simplifies the installation of MediaPipe for Windows devices, 10 and later. 

MediaPipe is not supported by Python 3.13.5, the latest Python release as at August 2nd 2025. 

To use MediaPipe for Gesture Control in VsCode requires the installation of Python 3.12 versions, I used Python 3.12.10, you can find it here 
[Python 3.12.10 download link](https://www.python.org/downloads/release/python-31210/) 

Media Pipe comes with an installation of OpenCV, numpy, matplotlib, and other Python libraries, so installing the Python 3.12.10 version is suitable for the essential Python functions which we may need for Engineering purposes. 

If newer versions were installed beforehand e.g Python 3.13, and the user wishes to use that Python version, switching only when a MediaPipe dependency is required, then a virtual enviroment is created to allow for the switching of interpreters. 

When using mediapipe however, it is recommended that you create a virtual environment to avoid dependency issues especially in production or multiproject setups.

## Installing Media Pipe
1. **Install Python 3.12**

    - Go to the Python 3.12 downloads page [Python 3.12.10 download link](https://www.python.org/downloads/release/python-31210/)

    - Download Windows installer (64-bit).

    - Run the installer:
        - Check “Add Python to PATH” before clicking Install.

2. **Verify installation in PowerShell or CMD**

Open PowerShell/CMD and run 

```powershell 
python --version
```

or 

```powershell
python3 --version
```

Should show something like

```text
Python 3.12.x
``` 

3. **Create Virtual Environment**

Navigate to your Project Folder, then in bash:

```bash 
python -m venv mediapipe_env
```

Check that you now have a folder in your Project like:
```text
mediapipe_env\
Scripts\
pyvenv.cfg
```    

4. **Activate Virtual Environment**     
Run in powershell from the same folder where ```mediapipe_env``` is located

```powershell
.\mediapipe_env\Scripts\Activate.ps1
```

If you see an “execution policy” error, type this in PowerShell

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
Then run the earlier activation command again 

5. **Install MediaPipe**

Type in bash
```bash 
pip install mediapipe
```

N.B: If you receive this error message:

```text
Error message:  A new release of pip is available: 25.0.1 -> 25.2
```

It's not an error, it’s just a notification telling you a newer version of pip is available.

**To upgrade pip (recommended)**

While inside your activated venv 
```((mediapipe_env)``` should show in prompt):

Type in bash
```bash 
python -m pip install --upgrade pip
```
**Then install MediaPipe**
In bash, type:
```bash 
pip install mediapipe
```

6. **Other Possible Errors**

One possible error ```WinError 32``` could occur when another process (like Antivirus, Windows Search Indexer, or even Explorer Preview) locks the file when the pip is trying to unpack/install it. 

```text
ERROR: Could not install packages due to an OSError: [WinError 32] The process cannot access the file because it is being used by another process: 
```
**Process to Fix it**
1. Close Interferring Programs or terminals in Vs Code or any other IDEs

2. Clear pip's temporary cache 

In powershell:
```powershell
pip cache purge
```
3. Retry Installation 

In powershell:
```powershell
pip install mediapipe
```
4. If issue persists — specify ```--no-cache-dir``` in powershell
This forces pip not to reuse cached files:

```powershell
pip install --no-cache-dir mediapipe
```

5. (Optional) Upgrade pip first

Sometimes upgrading pip fixes file-lock issues. Type in powershell:

```powershell
python -m pip install --upgrade pip
``` 
Then retry installing MediaPipe.

6. Run PowerShell as Administrator
Right-click PowerShell → Run as Administrator, activate venv, and install again.

## Verify Installation

1. Type in power shell inside ```mediapipe_env```

```powershell
pip list
```

Look for something like 
```nginx
mediapipe      0.10.x
```
2. Import Test in Python 
Run Python inside the venv

```powershell 
python
```

Then type:
```python 
import mediapipe as mp
print(mp.__version__)
```
---
© STEMAIDE 2025 - Internal Report
