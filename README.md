# Setting up with PyCharm on Mac M1/M2
To do this, make sure the project is created at Python 3.9 as some of the libraries don't work yet for 3.10.

Some of this may need revising as the process for getting here was pretty iterative.

STEPS:
- Install the tensorflow-macos and tensorflow-metal packages
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
- Install protobuf by downloading the right archive from [https://github.com/protocolbuffers/protobuf/releases](https://github.com/protocolbuffers/protobuf/releases). For M1/2 Macs this is the osx universal binary. Copy the binary somewhere and add the path to /etc/paths.
- Research models are cloned from github [https://github.com/tensorflow/models](https://github.com/tensorflow/models)
  - To generate the Python files, from the models/research folder and a terminal in the correct venv for the Python version you're using:
  ```commandline
  protoc object_detection/protos/*.proto --python_out=.
  cp object_detection/packages/tf2/setup.py . 
  ```
  - Need to pip install them from the tf2 setup:
  ```commandline
  cd ../models/research
  python -m pip install --no-deps .
  ```
  Note the --no-deps flag here! This is because the models package has a dependency on tensorflow which isn't used by MacOS users. We're using tensorflow-macos.

  