from asyncio import TaskGroup
from os.path import expandvars
from pathlib import Path
from shutil import rmtree

from loguru import logger


async def directory_files(directory: Path) -> None:
    for item in directory.iterdir():
        if not item.is_file():
            continue

        try:
            item.unlink()  # deletando um arquivo.
            logger.success(item.absolute())
        except PermissionError:
            logger.error(item.absolute())


async def directory_dirs(directory: Path) -> None:
    for item in directory.iterdir():
        if not item.is_dir():
            continue

        item_path = item.absolute()

        try:
            rmtree(item_path)  # deletando uma pasta.
            logger.success(item_path)
        except PermissionError:
            logger.error(item_path)


async def process(tasks: list) -> None:
    logger.debug(f"{len(tasks)} tarefas vão ser preparadas")
    paths = [path for task in tasks for path in task]
    logger.debug(f"{len(paths)} caminhos configurados")

    async with TaskGroup() as task_group:
        for string_path in paths:
            path = Path(string_path)

            if not path.exists():
                env_path = expandvars(string_path)
                path = Path(env_path)

            if not path.exists():
                logger.critical(path.absolute())
                continue

            task_group.create_task(directory_dirs(path))
            task_group.create_task(directory_files(path))

        logger.debug(f"Tarefa {paths.index(string_path)} finalizada")


if __name__ == "__main__":
    ...
