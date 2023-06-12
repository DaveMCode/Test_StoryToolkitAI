# StoryToolkitAI Installation Instructions

[Click here to the main project page](https://github.com/octimot/StoryToolkitAI)

## Installing the Standalone version
If you don't want to get your hands dirty with terminal commands, check if there is a release available for your 
platform [here](https://github.com/octimot/StoryToolkitAI/releases).

We do, however, recommend doing your best to install the non-standalone version of the tool using the instructions
below. This would allow you to get the latest features and bug fixes as soon as they are released.

### StoryToolkitAI is free but we need your help

The development of Storytoolkit AI depends highly on the support we get from our Patreon community, so
[please consider supporting the development](https://www.patreon.com/StoryToolkitAI) if you find this tool useful
in your work.

---

## Installing the Non-Standalone version

### Quick Info before we start

#### Caution
If you want to try to install a non-standalone version, please keep in mind that you might end up ruining your computer, 
destroying the Internet, starting AI apocalypse, losing your job, and/or marry your lost non-identical twin by mistake - 
not necessarily in that order and highly unlikely as a result of trying to install this, but still slightly possible. 

Nevertheless, we're not responsible for any of it or anything else that might happen. In a low-chance worst-case 
scenario, some stuff might not work at all on your computer, and you'll need pro help to fix them back.

#### Requirements

Our installations are on MacOS 12.6+ running on M1 and Windows 10 machines in our editing room, 
but the scripts should run fine on other CPUs and GPUs. 
For both production and development we're currently using Python 3.10.11. 

_Note: The tool worked fine on Python 3.9, but some packages are now optimized for Python 3.10. 
Python 3.9 support will no longer be possible in the very near future._

**The Resolve API integration only works on Resolve Studio 18 (not on the free version, and certainly not earlier 
versions).**

## Mac OS
In the Terminal:

#### 1. You'll need Homebrew

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

In case Homebrew installation fails, please check [this page](https://docs.brew.sh/Common-Issues) for troubleshooting.

One of the most common installation fails is due to the fact that Xcode Command Line Tools is not installed on your 
Mac, so you could try to install them first with `xcode-select --install`

#### 2. You'll need Python 3.10, Python Tkinter, Git, and FFMPEG:

    brew install python@3.10
    brew install python-tk@3.10
    brew install git
    brew install ffmpeg

#### 3. Install virtualenv:

We recommend running the tool inside a virtual environment like virtualenv. This is not required, but it prevents
messing up your Python installation, for that, you need to install virtualenv:

    python3.10 -m pip install virtualenv

_Note: if the pip command above doesn't work, try to use pip3 (and use pip3 for the next steps too)_

#### 4. Download StoryToolkitAI:
First, go to the Folder you want to install StoryToolkit in via Finder. Right-click on it and select "New Terminal at Folder".
Once you get another terminal window open, run:

    git clone git@github.com:octimot/StoryToolkitAI.git

This should download the app in the folder that you chose.

#### 5. Set up a virtual environment
Now create a virtual environment (to prevent messing up with other python packages you may have installed on your OS for other stuff):

    python3.10 -m virtualenv -p python3.10 venv

Right now, your installation folder should contain 2 other folders, and the tree should look like this:

    YOUR_INSTALLATION_FOLDER
    +- StoryToolkitAI
    +- venv

#### 6. Activate virtual environment
Now enable the virtual environment (this means that all the packages you'll install now via pip will be contained in the
virtual environment, meaning that for the tool to work you'll ALWAYS have to activate the virtual environment first
using the following command!)

    source venv/bin/activate

#### 7. Install OpenAI Whisper
_Note: starting with step 7, you need to make sure that you are installing packages inside the virtual environment. 
If you followed the previous steps, your terminal prompt should now have `(venv)` before everything else._

    pip install -U git+https://github.com/openai/whisper.git@248b6cb124225dd263bb9bd32d060b6517e067f8

For more info regarding Whisper installation, please check https://github.com/openai/whisper 

If you are seeing an error message like `error: subprocess-exited-with-error` (or similar), 
you might need to install rust first. If you already installed homebrew, it should be as easy as `brew install rust`,
if things get uneasy, see the instructions [here](https://www.rust-lang.org/learn/get-started)

#### 8. Install all the stuff the tool requires:
_Note: starting with step 7, you need to make sure that you are installing packages inside the virtual environment. 
If you followed the previous steps, your terminal prompt should now have `(venv)` before everything else._

    pip install -r StoryToolkitAI/requirements.txt

If you are running the tool on a machine with an NVIDIA CUDA GPU, make sure you install Torch with CUDA:

    pip uninstall torch
    pip cache purge
    pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116

_Note: If Resolve Studio is not turned on or not available, the transcription and translation functions will work on 
normal wav files too. Simply press the transcribe or translate buttons and follow the process._

#### That's it!
Inside the virtual environment, you should now be able to start the tool:

    python StoryToolkitAI/storytoolkitai

_Note: After restart of the machine or your terminal window, never forget to activate the virtual environment before
starting the app. In the folder where you created venv, run:_

    source venv/bin/activate
    
## Windows

#### 0. Open Command Prompt
First, create the folder where you want to install StoryToolkitAI. 
Then, open the Command Prompt and navigate to that folder - with Windows Explorer open in the installation folder,
type in `cmd` in the location bar above then press Enter, and your Command Prompt should start directly in the
installation folder.

#### 1. Download and install Python
Download the latest Python 3.10 version from [the official Python website](https://www.python.org/downloads/).

_Note: only use other Python installers / versions if you know what you're doing._

Then simply install it on your machine using the default settings.

To check if you installed the right version, open the Command Prompt and run:

    py --version

And something like `Python 3.10.11` should appear. Anything else besides 3.10.X means that you're in uncharted
territories! If that is the case, we recommend uninstalling all Python versions (if you don't need them of course)
and reinstalling Python 3.10.

#### 2. Download and install GIT for Windows
Download it from [here](https://git-scm.com/download/win) and then install it.

#### 3. Install virtualenv

We recommend running the tool inside a virtual environment like virtualenv. This is not required, but it prevents
messing up your Python installation, for that, you need to install virtualenv.

If you installed Python according to step 1, this shouldn't be necessary. But to make sure that you have virtualenv,
simply run:

    py -3.10 -m pip install virtualenv

#### 4. Download StoryToolkitAI:

Open the Command Prompt and navigate to the folder where you want to install StoryToolkitAI. Then run:

    git clone https://github.com/octimot/StoryToolkitAI.git

#### 5. Set up a virtual environment
Now create a virtual environment (to prevent messing up with other python packages you may have installed on your OS
for other stuff):

    py -3.10 -m virtualenv venv

Right now, your installation folder should contain 2 other folders, and the tree should look like this:
    
    YOUR_INSTALLATION_FOLDER
    +- StoryToolkitAI
    +- venv

#### 6. Activate virtual environment
Now enable the virtual environment (this means that all the packages you'll install now via pip will be contained in the
virtual environment, meaning that for the tool to work **you'll ALWAYS have to activate the virtual environment first**
using the following command!)

    venv\Scripts\activate.bat

#### 7. Install OpenAI Whisper
Note: starting with step 7, you need to make sure that you are installing packages inside the virtual environment. If you followed the previous steps, your terminal prompt should now have (venv) before everything else.

    pip install -U git+https://github.com/openai/whisper.git@248b6cb124225dd263bb9bd32d060b6517e067f8

For more info regarding Whisper installation, please check https://github.com/openai/whisper

#### 8. Install all the stuff the tool requires:
Note: starting with step 7, you need to make sure that you are installing packages inside the virtual environment. 
If you followed the previous steps, your terminal prompt should now have (venv) before everything else.

    pip install -r StoryToolkitAI\requirements.txt

If you are running the tool on a machine with an NVIDIA CUDA GPU, make sure you install Torch with CUDA:
    
    pip uninstall torch torchaudio torchvision
    pip cache purge
    pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117

_Note: If Resolve Studio is not turned on or not available, the transcription and translation functions will work on 
normal wav files too. Simply press the transcribe or translate buttons and follow the process._

#### That's it!
Inside the virtual environment, you should now be able to start the tool:

    py StoryToolkitAI\storytoolkitai

_Note: After restart of the machine or your terminal window, never forget to activate the virtual environment before
starting the app. In the folder where you created venv, run:_

    venv\Scripts\activate.bat

_Note: if you're using a version earlier than 0.18.0, the old run command was: `python StoryToolkitAI/app.py`_

## Running the non-standalone tool

If you haven't downloaded the app in a binary format, simply activate the virtual environment and start the tool:

### On windows:

    venv\Scripts\activate.bat
    py StoryToolkitAI\storytoolkitai

### On Mac OS:

    source venv/bin/activate
    python StoryToolkitAI/storytoolkitai

The tool should pop up now on the screen

<img src="help/storytoolkitai_v0.19.0.png" width="600">

_Note: if you're using a version earlier than 0.18.0, the old run commands were: 
`python StoryToolkitAI/app.py`_ (macOS), or `py StoryToolkitAI\app.py` (Windows)

## Updates on the non-standalone tool
To update the tool, simply pull the latest changes from the repository while inside the folder where you installed the 
tool:

    git pull

Also make sure to always check for package updates after pulling a new version of the tool: 

     # on Windows
    pip install -r StoryToolkitAI\requirements.txt

    # on MacOS
    pip install -r StoryToolkitAI/requirements.txt

## Feedback

Feedback regarding these instructions is very welcome and might help others! 

Please let us know if you have any issues or suggestions for improvement via the 
[issues page](https://github.com/octimot/StoryToolkitAI/issues).
