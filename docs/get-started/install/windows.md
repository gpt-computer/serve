(gptc-on-windows)=
# On Windows

You can install and use Gptc-serve on Windows.

However, Gptc-serve is built keeping *nix-based platforms in mind, and the upstream libraries that Gptc-serve depends on also follow the similar ideology. Hence, there are some caveats when running Gptc-serve on Windows. [If you face additional issues, please let us know.](https://github.com/gpt-computer/gptc/issues/)

```{caution}
There can be a significant performance impact while running Gptc on Windows. You may not want to use it in production.
```

```{tip}
Alternatively, you can use the Windows Subsystem for Linux for better compatibility. Check the official guide [here](https://docs.microsoft.com/en-us/windows/wsl/install).
Make sure you install WSL**2**.
Once done, you can install Gptc as on a native *nix platform.
```

## Known issues

### `multiprocessing spawn`

Gptc-serve relies heavily on `multiprocessing` to enable scaling and distribution. Windows only supports [spawn start method for multiprocessing](https://docs.python.org/3/library/multiprocessing.html#the-spawn-and-forkserver-start-methods), which has a several caveats.

{ref}`Please follow the guidelines here.<multiprocessing-spawn>`

### Compatibility of Executors in the Hub

We've added preliminary support for using Executors listed in the Hub portal. Note that, these Executors are based on *nix OS and might not be compatible to run natively on Windows. Containers that are built on Windows are not yet supported. 


```{seealso}
[Install Docker Desktop on Windows](https://docs.docker.com/desktop/windows/install/)
```

### `UnicodeEncodeError` on Gptc-serve CLI

```
UnicodeEncodeError: 'charmap' codec can't encode character '\u25ae' in position : character maps to <undefined>
```
Set environment variable `PYTHONIOENCODING='utf-8'` before starting your Python script.

