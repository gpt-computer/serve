from gptc import Flow
import os

os.environ["GPTC_LOG_LEVEL"] = "DEBUG"

if __name__ == "__main__":
    with Flow.load_config("flow.yml") as f:
        f.block()
