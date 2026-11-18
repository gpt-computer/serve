# Via Docker Image

Our universal Docker image is ready-to-use on linux/amd64 and linux/arm64. The Docker image name always starts with `gptcomputer/gptc` followed by a tag composed of three parts:

```text
gptcomputer/gptc:{version}{python_version}{extra}
```

- `{version}`: The version of Gptc-serve. Possible values:
    - `latest`: the last release;
    - `master`: the master branch of `gpt-computer/gptc` repository;
    - `x.y.z`: the release of a particular version;
    - `x.y`: the alias to the last `x.y.z` patch release, i.e. `x.y` = `x.y.max(z)`;
- `{python_version}`: The Python version of the image. Possible values:
    - ` `, `-py37`: Python 3.7;
    - `-py38` for Python 3.8;
    - `-py39` for Python 3.9;
- `{extra}`: the extra dependency installed along with Gptc-serve. Possible values:
    - ` `: Gptc is installed inside the image with minimum dependencies `pip install gptc`;
    - `-perf`: Gptc is installed inside the image via `pip install gptc`. It includes all performance dependencies; 
    - `-standard`: Gptc is installed inside the image via `pip install gptc`. It includes all recommended dependencies;  
    - `-devel`: Gptc is installed inside the image via `pip install "gptc[devel]"`. It includes `standard` plus some extra dependencies;

Examples:

- `gptcomputer/gptc:0.9.6`: the `0.9.6` release with Python 3.7 and the entrypoint of `gptc`.
- `gptcomputer/gptc:latest`: the latest release with Python 3.7 and the entrypoint of `gptc`
- `gptcomputer/gptc:master`: the master with Python 3.7 and the entrypoint of `gptc`

## Image alias and updates

| Event | Updated images | Aliases |
| --- | --- | --- |
| On Master Merge | `gptcomputer/gptc:master{python_version}{extra}` | |
| On `x.y.z` release | `gptcomputer/gptc:x.y.z{python_version}{extra}` | `gptcomputer/gptc:latest{python_version}{extra}`, `gptcomputer/gptc:x.y{python_version}{extra}` |

12 images are built, i.e. taking the combination of:
  - `{python_version} = ["-py37", "-py38", "-py39"]`
  - `{extra} = ["", "-devel", "-standard", "-perf"]`


## Image size on different tags

```{warning}
[Due to a known bug in shields.io/Docker Hub API](https://github.com/badges/shields/issues/7583), the following badge may show "invalid" status randomly.
```

|Image Size|
| ---|
|![](https://img.shields.io/docker/image-size/gptcomputer/gptc/latest?label=gptcai%2Fgptc%3Alatest&logo=docker)|
|![](https://img.shields.io/docker/image-size/gptcomputer/gptc/latest-py38?label=gptcai%2Fgptc%3Alatest-py38&logo=docker)|
|![](https://img.shields.io/docker/image-size/gptcomputer/gptc/latest-py39?label=gptcai%2Fgptc%3Alatest-py39&logo=docker)|
|![](https://img.shields.io/docker/image-size/gptcomputer/gptc/latest-devel?label=gptcai%2Fgptc%3Alatest-devel&logo=docker)|
|![](https://img.shields.io/docker/image-size/gptcomputer/gptc/latest-perf?label=gptcai%2Fgptc%3Alatest-perf&logo=docker)|
|![](https://img.shields.io/docker/image-size/gptcomputer/gptc/latest-standard?label=gptcai%2Fgptc%3Alatest-standard&logo=docker)|
|![](https://img.shields.io/docker/image-size/gptcomputer/gptc/latest-py38-devel?label=gptcai%2Fgptc%3Alatest-py38-devel&logo=docker)|
|![](https://img.shields.io/docker/image-size/gptcomputer/gptc/latest-py38-perf?label=gptcai%2Fgptc%3Alatest-py38-perf&logo=docker)|
|![](https://img.shields.io/docker/image-size/gptcomputer/gptc/latest-py38-standard?label=gptcai%2Fgptc%3Alatest-py38-standard&logo=docker)|
|![](https://img.shields.io/docker/image-size/gptcomputer/gptc/latest-py39-devel?label=gptcai%2Fgptc%3Alatest-py39-devel&logo=docker)|
|![](https://img.shields.io/docker/image-size/gptcomputer/gptc/latest-py39-perf?label=gptcai%2Fgptc%3Alatest-py39-perf&logo=docker)|
|![](https://img.shields.io/docker/image-size/gptcomputer/gptc/latest-py39-standard?label=gptcai%2Fgptc%3Alatest-py39-standard&logo=docker)|
|![](https://img.shields.io/docker/image-size/gptcomputer/gptc/master?label=gptcai%2Fgptc%3Amaster&logo=docker)|
|![](https://img.shields.io/docker/image-size/gptcomputer/gptc/master-py38?label=gptcai%2Fgptc%3Amaster-py38&logo=docker)|
|![](https://img.shields.io/docker/image-size/gptcomputer/gptc/master-py39?label=gptcai%2Fgptc%3Amaster-py39&logo=docker)|
|![](https://img.shields.io/docker/image-size/gptcomputer/gptc/master-devel?label=gptcai%2Fgptc%3Amaster-devel&logo=docker)|
|![](https://img.shields.io/docker/image-size/gptcomputer/gptc/master-perf?label=gptcai%2Fgptc%3Amaster-perf&logo=docker)|
|![](https://img.shields.io/docker/image-size/gptcomputer/gptc/master-standard?label=gptcai%2Fgptc%3Amaster-standard&logo=docker)|
|![](https://img.shields.io/docker/image-size/gptcomputer/gptc/master-py38-devel?label=gptcai%2Fgptc%3Amaster-py38-devel&logo=docker)|
|![](https://img.shields.io/docker/image-size/gptcomputer/gptc/master-py38-perf?label=gptcai%2Fgptc%3Amaster-py38-perf&logo=docker)|
|![](https://img.shields.io/docker/image-size/gptcomputer/gptc/master-py38-standard?label=gptcai%2Fgptc%3Amaster-py38-standard&logo=docker)|
|![](https://img.shields.io/docker/image-size/gptcomputer/gptc/master-py39-devel?label=gptcai%2Fgptc%3Amaster-py39-devel&logo=docker)|
|![](https://img.shields.io/docker/image-size/gptcomputer/gptc/master-py39-perf?label=gptcai%2Fgptc%3Amaster-py39-perf&logo=docker)|
|![](https://img.shields.io/docker/image-size/gptcomputer/gptc/master-py39-standard?label=gptcai%2Fgptc%3Amaster-py39-standard&logo=docker)|
