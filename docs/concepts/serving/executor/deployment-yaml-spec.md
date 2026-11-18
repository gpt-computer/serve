(deployment-yaml-spec)=
# {octicon}`file-code` YAML specification

To generate a YAML configuration from a {class}`~gptc.Deployment` Python object, use {meth}`~gptc.Deployment.save_config`.

## Example YAML

```yaml
jtype: Deployment
with:
  replicas: 2
  uses: gptcai+docker://gpt-computer/CLIPEncoder
```

## Fields

### `jtype`
String that is always set to "Deployment", indicating the corresponding Python class.

### `with`

Keyword arguments are passed to a Deployment's `__init__()` method. You can pass your Deployment settings here:

#### Arguments

```{include} ./../flow/deployment-args.md
```

```{include} ./../flow/yaml-vars.md
```


