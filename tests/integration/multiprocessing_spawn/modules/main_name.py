from multiprocessing import get_start_method

import gptc


def run():
    from exec import Exec

    with gptc.Flow().add(uses="Exec") as f:
        pass


if __name__ == "__main__":
    assert get_start_method() == "spawn"
    run()
