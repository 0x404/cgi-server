# Contributing Guide
Thank you for investing your time in contributing to our project!

## New contributor guide

To get an overview of the project, read the [README](../readme.md). Here are some resources to help you get started with open source contributions:

- [Finding ways to contribute to open source on GitHub](https://docs.github.com/en/get-started/exploring-projects-on-github/finding-ways-to-contribute-to-open-source-on-github)
- [Set up Git](https://docs.github.com/en/get-started/quickstart/set-up-git)
- [GitHub flow](https://docs.github.com/en/get-started/quickstart/github-flow)
- [Collaborating with pull requests](https://docs.github.com/en/github/collaborating-with-pull-requests)

## Getting started

### Set up your dev environment

The version of python we are using should >= **3.9**

Currently we rely on [`black`](https://github.com/psf/black) and [`pylint`](https://pylint.pycqa.org/en/latest/) to do code static analysis checks. Use the following command to install:

```shell
pip3 install -r requirements.txt
```

Regarding the use of black, when you use the following command, black will automatically format all python files in the current directory.

```shell
black .
```

Regarding the use of pylint, when you use the following command, pylint will automatically check the python code in the `cgiserver` directory, and if there is an error, it will list the location and cause of the error.

You need to fix these errors or close these errors. For more usage, please refer to the [pylint documentation](https://pylint.pycqa.org/en/latest/)
```shell
pylint cgiserver
```

It should be noted that when you open a PR, github action will automatically perform black and pylint checks on your code, **so please pay attention to passing the local check before submitting the code**. The local check script is in [tests directory](../scripts/). If you are a Windows user, you can also view the script and complete the check in a similar way.
