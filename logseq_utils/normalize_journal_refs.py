import glob
import re

from pathlib import Path
from tqdm import tqdm

def transform_date(content: str) -> str:
    """
    Transforms date references in double square brackets inside `content` from format [[Month Day, Year]] to format [[Year/Month/Day]].
    
    Args:
        content (str): The content in which dates need to be transformed.
    
    Returns:
        str: The content with all dates transformed to the new format.    
    """
    pattern = r'\[\[(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{1,2}[a-zA-Z]*), (\d{4})\]\]'
    
    def replacer(match):
        month, day, year = match.groups()
        month_num = {
            'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
            'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
            'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
        }[month]
        day = re.sub(r'[a-zA-Z]+', '', day)
        return f"[[{year}-{month_num}-{day.zfill(2)}]]"
    
    return re.sub(pattern, replacer, content)

def replace_dates_in_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    new_content = transform_date(content)
    
    with open(file_path, 'w') as f:
        f.write(new_content)

def rename_file(file_path):
    file_path = Path(file_path)
    new_file_path = file_path.with_name(transform_date(file_path.name))
    # only proceed if the new file path is different from the old one
    if new_file_path == file_path:
        return file_path
    print(f"Renaming {file_path} to {new_file_path}")
    file_path.rename(new_file_path)
    return new_file_path


def main():
    # loop over all markdown files in the current directory
    for file_path in tqdm(Path.cwd().glob("*.md")):
        assert file_path.is_file()
        assert file_path.suffix == ".md"
        replace_dates_in_file(file_path)
        rename_file(file_path)


if __name__ == "__main__":
    # # test the function
    # assert transform_date("This is a test [[Jan 1st, 2020]]") == "This is a test [[2020/01/01]]"
    # assert transform_date("This is a test [[Oct 31st, 2020]]") == "This is a test [[2020/10/31]]"
    # assert transform_date("This should not be changed [[2020/10/31]]") == "This should not be changed [[2020/10/31]]"
    # assert transform_date("This should not be changed [Oct 31st, 2020]") == "This should not be changed [Oct 31st, 2020]"
    # print("All tests passed!")

    main()
    