# Interactive Broker Package Installation

## Step 1: Get a list of all the libraries you need to install the package

Most python packages will have other packages they use to run, these packages that fall outside of the standard python packages must be specified before we can run the install the package. I did a little research and found that there was a python package called `pipreqs` that will specify the packages you require for installation. If we use `pip freeze` it will return all the python packages we have installed even if the package doesn't require them.

To install `pipreqs` run the following command:

```console
pip install pipreqs
```

After you've done that, you specify the path to pacakge, the general syntax is as follows:

```console
pipreqs /path/to/project
```

I use Windows, so when I ran the command it looked like the following:

```console
pipreqs ..\interactive-broker-python-api
```

Now if you already have a `requirements.txt` file in the folder, `pipreqs` won't overwrite it unless you specify the `--force` argument. That means if you want to overwrite the existing `requirements.txt` file run the following command:

```console
pipreqs ..\interactive-broker-python-api --force
```

## Step 2: Create `setup.py` File

First part of distributing a Python package is specifying a `setup.py` file which will list all the requirements needed to use the package, metadate like who built it, license information, and the python version needed to run the package. In the folder you'll notice I have a `setup.py` file which specifies the following.

```python
from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
      name='Interactive Broker Unofficial Web API',
      author='Alex Reed',
      author_email='coding.sigma@gmail.com',
      version='0.1.0',
      description='A python client lirbary for the Interactive Broker Web API.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/areed1192/interactive-broker-python-api',
      install_reqs = [
            'certifi==2019.11.28',
            'requests==2.22.0',
            'urllib3==1.25.3'
      ],
      packages=['ibw'],
      classifiers=[
           'Development Status :: 3 - Alpha',
           'Intended Audience :: Financial and Insurance Industry',
           'License :: OSI Approved :: MIT License',
           'Natural Language :: English',
           'Operating System :: OS Independent',
           'Programming Language :: Python :: 3'
      ],
      python_requires='>=3.7'
     )
```

## Step 3: Install the package in Development Mode

Now that we have a `setup.py` file we can install our package. Since it's still a work in progress I recommend you install it in `development mode`. What that means is it will install the package in the local directory. That means you can import the libraries like you normally would if you had installed it in the normal fashion.

To install a python package in `development mode` you specify the `-e` argument which is short for `--editable`. In addition, if you're already in the `root directory` then all you need to specify is `- e .`

Here is how it looks if you are in the `root directory`:

```console
pip install -e .
```

If you aren't in the root directory just specify the file path like so:

```console
pip install -e "<PATH TO DIRECTORY>"
```
