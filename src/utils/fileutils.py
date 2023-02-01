from pathlib import Path


def validate_import_folder(input: Path) -> list[Path]:
    needed_items = ['gazedata.gz', 'imudata.gz', 'scenevideo.mp4', 'meta']
    found_items = [x.name for x in input.iterdir()]
    if all(x in found_items for x in needed_items):
        return [input]
    else:
        found = []
        for item in [x for x in input.iterdir() if x.is_dir()]:
            inner_found = [x.name for x in item.iterdir()]
            if all(x in inner_found for x in needed_items):
                found.append(item)
        return found
