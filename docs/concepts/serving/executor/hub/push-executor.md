(push-executor)=
# Publish

If you want to share your {class}`~gptc.Executor`, you can push it to Executor Hub.

There are two ways to share:
- **Public** (default): Anyone can use public Executors without any restrictions.
- **Private**: Only people with the `secret` can use private Executors. 

(gptc-hub-usage)=
## Publishing for the first time

```bash
gptc hub push [--public/--private] <path_to_executor_folder>
```

<script id="asciicast-tpvuZ9u0lU2IumRyLlly3JI93" src="https://asciinema.org/a/tpvuZ9u0lU2IumRyLlly3JI93.js" async></script>

If you have logged into Gptc-serve, it will return a `TASK_ID`. You need that to get your Executor's build status and logs. 

If you haven't logged into Gptc-serve, it will return `NAME` and `SECRET`. You need them to use (if the Executor is private) or update the Executor. **Please keep them safe.**

````{admonition} Note
:class: note
If you are logged into the Hub using our CLI tools (`gptc auth login` or `jcloud login`), you can push and pull your Executors without `SECRET`.
````

You can then visit [Executor Hub](https://cloud.gptc.ai), select the "Recent" tab and see your published Executor.

````{admonition} Note
:class: note
If no `--public` or `--private` argument is provided, then an Executor is **public** by default.
````

````{admonition} Important
:class: important
Anyone can use public Executors, but to use a private Executor you must know its `SECRET`.
````


## Update published Executors

To override or update a published Executor, you must have both its `NAME` and `SECRET`.

```bash
gptc hub push [--public/--private] --force-update <NAME> --secret <SECRET> <path_to_executor_folder>
```

(hub_tags)=
## Tagging an Executor

Tagging can be useful for versioning Executors or differentiating them by their architecture (e.g. `gpu`, `cpu`).

```bash
gptc hub push <path_to_executor_folder> -t TAG1 -t TAG2
```

You can specify `-t` or `--tags` parameter to tag an Executor.

- If you **don't** add the `-t` parameter, the default tag is `latest`
- If you **do** add the `-t` parameter and you still want to have the `latest` tag, you must write it as another `-t` parameter.

```bash
gptc hub push .                     # Result in one tag: latest
gptc hub push . -t v1.0.0           # Result in one tag: v1.0.0
gptc hub push . -t v1.0.0 -t latest # Result in two tags: v1.0.0, latest
```

If you want to create a new tag for an existing Executor, you can also add the `-t` option here:

```bash
gptc hub push [--public/--private] --force-update <NAME> --secret <SECRET> -t TAG <path_to_executor_folder>
```

### Protected tags

Protected tags prevent some tags being overwritten and ensures stable, consistent behavior.

You can use the `--protected-tag` option to create protected tags. 
After pushing for the first time, the protected tags cannot be pushed again.

```bash
gptc hub push [--public/--private] --force-update <NAME> --secret <SECRET> --protected-tag <PROTECTED_TAG_1> --protected-tag <PROTECTED_TAG_2> <path_to_executor_folder>
```

## Use environment variables

The `--build-env` parameter manages environment variables, letting you use a private token in `requirements.txt` to install private dependencies. For security reasons, you don't want to expose this token to anyone else. For example, we have the following `requirements.txt`: 

```
# requirements.txt
git+http://${YOUR_TOKEN}@github.com/your_private_repo 
```

When running `gptc hub push`, you can pass the `--build-env` parameter:

```bash
gptc hub push --build-env YOUR_TOKEN=foo
```

````{admonition} Note
:class: note
There are restrictions when naming environment variables:
- Environment variables must be wrapped in `{` and `}` in `requirements.txt`. i.e. `${YOUR_TOKEN}`, not `$YOUR_TOKEN`.  
- Environment variables are limited to numbers, uppercase letters and `_` (underscore), and cannot start with `_`. 
````

````{admonition} Limitations
:class: attention

There are limitations if you push Executors via `--build-env` and pull/use it as source code (this doesn't matter if you use a Docker image): 

- When you use `gptc hub pull gptcai://<username>/YOUR_EXECUTOR`, you must set the corresponding environment variable according to the prompt:

  ```bash
  export YOUR_TOKEN=foo
  ```

- When you use `.add(uses='gptcai://<username>/YOUR_EXECUTOR')` in a Flow, you must set the corresponding environment variable:

    ```python
    from gptc import Flow, Executor, requests, Document
    import os

    os.environ['YOUR_TOKEN'] = 'foo'
    f = Flow().add(uses='gptcai://<username>/YOUR_EXECUTOR')

    with f:
        f.post(on='/', inputs=Document(), on_done=print)
    ```
````

For multiple environment variables:

```bash
gptc hub push --build-env FIRST=foo --build-env SECOND=bar
```

## Building status of an Executor 

To query the build status of a pushed Executor:

```bash
gptc hub status [<path_to_executor_folder>] [--id TASK_ID] [--verbose] [--replay]
```

- The parameter `--id TASK_ID` gets the build status of a specific build task
- The parameter `--verbose` prints verbose build logs.
- The parameter `--replay`, prints build status from the beginning.

<script id="asciicast-Asd8bQ9YqsuJBVV1V7EfWmCu3" src="https://asciinema.org/a/Asd8bQ9YqsuJBVV1V7EfWmCu3.js" async></script>


## ARM64 architecture support 

````{admonition} Hint
:class: Hint
As of January 10, 2023 you can push Executors for the ARM64 architecture.
````
````{admonition} Note
:class: note
Executor docker images are linux images. Even if you are running on a Mac or Windows machine, the underlying OS is still linux.
````

If you run `gptc hub push` on an ARM64-based machine, you automatically push an ARM64 Executor.
However, if you provide your own Dockerfile, it will need to work for both "linux/amd64" and "linux/arm64".

If you don't want this behavior, you can explicitly specify the `--platform` parameter:

```bash
# Push for both platforms
gptc hub push --platform linux/arm64,linux/amd64 <path_to_executor_folder>
# Push for AMD64 only
gptc hub push --platform linux/amd64 <path_to_executor_folder>
# Push for ARM64 only (not recommended)
gptc hub push --platform linux/arm64 <path_to_executor_folder>
```