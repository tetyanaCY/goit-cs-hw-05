import argparse
import asyncio
import logging
from aiopath import AsyncPath
from aioshutil import copyfile

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_args():
    parser = argparse.ArgumentParser(description="Asynchronously sort files from a source directory to an output directory based on file extensions.")
    parser.add_argument("--source", "-s", required=True, help="Path to the source folder.")
    parser.add_argument("--output", "-o", required=True, help="Path to the output folder.")
    return parser.parse_args()

async def read_folder(path: AsyncPath):
    async for file in path.iterdir():
        if await file.is_dir():
            await read_folder(file)
        else:
            await copy_file(file)

async def copy_file(file: AsyncPath):
    if file.suffix:
        folder_name = file.suffix[1:]
    else:
        folder_name = "no_extension"
    folder = output / folder_name
    await folder.mkdir(exist_ok=True, parents=True)
    dest_file = folder / file.name
    await copyfile(file, dest_file)
    logging.info(f"Copied {file} to {dest_file}")

async def main():
    args = parse_args()
    global source, output
    source = AsyncPath(args.source)
    output = AsyncPath(args.output)
    await read_folder(source)
    logging.info(f"All files have been copied to {output} and sorted based on their extensions.")

if __name__ == "__main__":
    asyncio.run(main())

