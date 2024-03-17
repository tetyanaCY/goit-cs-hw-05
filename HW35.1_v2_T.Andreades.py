import asyncio
import aiofiles
import aiofiles.os
import argparse
from pathlib import Path

# Ініціалізація парсера аргументів
parser = argparse.ArgumentParser(description="Asynchronously sort files from a source directory to a target directory based on file extension.")
parser.add_argument("--source", type=str, required=True, help="Path to the source folder.")
parser.add_argument("--target", type=str, required=True, help="Path to the output folder.")
args = parser.parse_args()

async def copy_file(src_path: Path, dest_path: Path):
    """
    Asynchronously copy a file from src_path to dest_path.
    """
    async with aiofiles.open(src_path, 'rb') as src_file:
        content = await src_file.read()
        async with aiofiles.open(dest_path, 'wb') as dest_file:
            await dest_file.write(content)

async def read_folder(source_path: Path, target_path: Path):
    """
    Recursively read files from the source directory and copy them to the target directory.
    """
    async for root, _, files in aiofiles.os.walk(source_path):
        for file in files:
            file_path = Path(root) / file
            # Extract file extension and create a target subdirectory
            extension = file_path.suffix[1:]  # Remove the dot
            if not extension:
                extension = "no_extension"
            extension_dir = target_path / extension
            if not extension_dir.exists():
                await aiofiles.os.mkdir(extension_dir)
            
            dest_path = extension_dir / file_path.name
            await copy_file(file_path, dest_path)

async def main():
    source_path = Path(args.source)
    target_path = Path(args.target)

    # Ensure target directory exists
    if not target_path.exists():
        await aiofiles.os.mkdir(target_path)

    await read_folder(source_path, target_path)

if __name__ == "__main__":
    asyncio.run(main())
