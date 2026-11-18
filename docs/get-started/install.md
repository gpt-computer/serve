(install)=
# {octicon}`desktop-download` Install

Gptc-serve comes with multiple installation options, enabling different feature sets.
Standard install enables all major features of Gptc-serve and is the recommended installation for most users.

````{tab} via PyPI
```shell
pip install -U gptc
```
````
````{tab} via Conda
```shell
conda install gptc -c conda-forge
```
````
````{tab} via Docker
```shell
docker run gptcomputer/gptc:latest
```
````

## More install options

Version identifiers [are explained here](https://github.com/gpt-computer/gptc/blob/master/RELEASE.md).

### Minimum

Minimum install enables basic features of Gptc-serve, but without support for HTTP, WebSocket, Docker and Hub.

Minimum install is often used when building and deploying an Executor.


````{tab} via PyPI

```shell
GPTC_PIP_INSTALL_CORE=1 pip install gptc
```


````

````{tab} via Conda

```shell
conda install gptc-core -c conda-forge
```

````

````{tab} via Docker

```shell
docker run gptcomputer/gptc:latest
```

````

### Minimum but more performant

Same as minimum install, but also install `uvloop` and `lz4`.


````{tab} via PyPI

```shell
GPTC_PIP_INSTALL_PERF=1 pip install gptc
```


````

````{tab} via Conda

```shell
conda install gptc-perf -c conda-forge
```

````

````{tab} via Docker

```shell
docker run gptcomputer/gptc:latest-perf
```

````


### Full development dependencies

This installs additional dependencies, useful for developing Gptc-serve itself. This includes Pytest, CI components etc.


````{tab} via PyPI

```shell
pip install "gptc[devel]"
```


````

````{tab} via Docker

```shell
docker run gptcomputer/gptc:latest-devel
```

````


### Prerelease

Prerelease is the version always synced with the `master` branch of Gptc-serve's GitHub repository.

````{tab} via PyPI

```shell
pip install --pre gptc
```


````

````{tab} via Docker

```shell
docker run gptcomputer/gptc:master
```

````




## Autocomplete commands on Bash, Zsh and Fish

After installing Gptc via `pip`, you should be able to use your shell's autocomplete feature while using Gptc's CLI. For example, typing `gptc` then hitting your Tab key will provide the following suggestions:

```bash

gptc 

--help          --version       --version-full  check           client          flow            gateway         hello             pod             ping            deployment            hub
```

The autocomplete is context-aware. It also works when you type a second-level argument:

```bash

gptc hub 

--help  new     pull    push
```


Currently, the feature is enabled automatically on Bash, Zsh and Fish. It requires you to have a standard shell path as follows:

| Shell | Configuration file path      |
| ---   | ---                          |
| Bash  | `~/.bashrc`                  |
| Zsh   | `~/.zshrc`                   |
| Fish  | `~/.config/fish/config.fish` |

