# Contributing to Eclair

Thank you for your interest in contributing to Eclair! We welcome contributions from the community to improve and enhance our project. Before getting started, please take a moment to review the guidelines below.

## Table of Contents

1. [How to Contribute](#how-to-contribute)
    - [Reporting Issues](#reporting-issues)
    - [Submitting Pull Requests](#submitting-pull-requests)
2. [Development Setup](#development-setup)
    - [Build and Test](#build-and-test)
    - [Environment Setup](#environment-setup)
    - [Dependency Graphs](#dependency-graphs)
3. [Contact](#contact)

## How to Contribute

### Reporting Issues

If you encounter a bug, have a feature request, or any other issue related to the project, please check the [existing issues](https://github.com/abhinavmir/eclair/issues) or open a new issue and provide as much detail as possible to help us understand and address the problem. Feel free to self-assign and start work. I'm reviewing PRs alone, so reach out if you want to help!

### Submitting Pull Requests

We encourage you to contribute to the project by submitting pull requests (PRs). Here's a general outline of the steps to follow:

1. Fork the repository to your GitHub account.
2. Create a new branch from the `main` branch for each feature/fix.
3. Make your changes and commit them with descriptive messages.
4. Push the changes to your branch in the forked repository.
5. Submit a PR from your branch to the `main` branch of this repository.

Naming convention: @uname + (feature or fix) + issue-

## Development Setup

To set up your local development environment, follow these steps:

### Build and Test

1. Install Just
Instructions [here](https://github.com/casey/just#installation), but `<package manager> <install/add> just` should work for most platforms.

2. To build the project and run tests, execute the following command:

```bash
just env
just activate
just requirements # installs requirements
just clean-build # builds the project
```

(Open an issue if you have trouble with this step)

### Dependency Graphs

To generate dependency graphs, run:

```bash
just dependency
```

## Contact

Refer to [README.md](README.md)