# Setting up with PyCharm on Mac M1/M2
To do this, make sure the project is created at Python 3.9 as some of the libraries don't work yet for 3.10.

for Mac:
- Install the tensorflow-macos package
- tensorflow-text needs a download of the .whl from [github](https://github.com/sun1638650145/Libraries-and-Extensions-for-TensorFlow-for-Apple-Silicon/releases)
  - Note that the 38 / 39 etc relate to the Python version i.e. 38 is for Python 3.8
  - To install, from inside the console in the venv 
    ```commandline
    pip install [path to folder]/tensorflow_text-2.9.0-cp39-cp39-macosx_11_0_arm64.whl
    ```
- tensorflow-io is needed but for macos a whl needs to be built.
  - I cloned a project [https://github.com/tensorflow/io.git](https://github.com/tensorflow/io.git) in my home folder
  ```commandline
  git clone https://github.com/tensorflow/io.git
  cd io
  python3 setup.py -q bdist_wheel
  ```
  I've done that now and created whl files for Python 3.9 and 3.10 so don't need to do that again.
  - To install one of those whls, from the terminal in PyCharm (inside the venv), run:
  ```commandline
  python3 -m pip install --no-deps  tensorflow_io-0.27.0-cp39-cp39-macosx_10_9_universal2.whl
  ```
- Research models are cloned from github [https://github.com/tensorflow/models](https://github.com/tensorflow/models)
  - Need to pip install them from the tf2 setup I already copied to the research folder:
  ```commandline
  cd ../models/research
  python -m pip install --no-deps .
  ```
  Note the --no-deps flag here! This is because the models package has a dependency on tensorflow which isn't used by MacOS users. We're using tensorflow-macos.

  