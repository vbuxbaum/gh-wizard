import os
import numpy as np
from rich import print
import datetime
from git import Repo
from pathlib import Path

MULTIPLIER = 20
PIXEL_MATRIX = [
    [1.0, 0.7, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.7, 1.0, 0.7, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.7, 1.0, 0.7, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.7, 1.0, 0.7, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.7, 1.0, 0.7, 0.4, 0.0],
    [0.7, 1.0, 0.7, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.7, 1.0, 0.7, 1.0, 0.7, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.7, 1.0, 0.7, 1.0, 0.7, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.7, 1.0, 0.7, 1.0, 0.7, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.7, 1.0, 0.7, 1.0, 0.7, 0.4],
    [0.4, 0.7, 1.0, 0.7, 0.4, 0.0, 0.0, 0.0, 0.4, 0.7, 1.0, 0.7, 0.4, 0.7, 1.0, 0.7, 0.4, 0.0, 0.0, 0.0, 0.4, 0.7, 1.0, 0.7, 0.4, 0.7, 1.0, 0.7, 0.4, 0.0, 0.0, 0.0, 0.4, 0.7, 1.0, 0.7, 0.4, 0.7, 1.0, 0.7, 0.4, 0.0, 0.0, 0.0, 0.4, 0.7, 1.0, 0.7, 0.4, 0.7, 1.0, 0.7],
    [0.0, 0.4, 0.7, 1.0, 0.7, 0.4, 0.0, 0.4, 0.7, 1.0, 0.7, 0.4, 0.0, 0.4, 0.7, 1.0, 0.7, 0.4, 0.0, 0.4, 0.7, 1.0, 0.7, 0.4, 0.0, 0.4, 0.7, 1.0, 0.7, 0.4, 0.0, 0.4, 0.7, 1.0, 0.7, 0.4, 0.0, 0.4, 0.7, 1.0, 0.7, 0.4, 0.0, 0.4, 0.7, 1.0, 0.7, 0.4, 0.0, 0.4, 0.7, 1.0],
    [0.0, 0.0, 0.4, 0.7, 1.0, 0.7, 0.4, 0.7, 1.0, 0.7, 0.4, 0.0, 0.0, 0.0, 0.4, 0.7, 1.0, 0.7, 0.4, 0.7, 1.0, 0.7, 0.4, 0.0, 0.0, 0.0, 0.4, 0.7, 1.0, 0.7, 0.4, 0.7, 1.0, 0.7, 0.4, 0.0, 0.0, 0.0, 0.4, 0.7, 1.0, 0.7, 0.4, 0.7, 1.0, 0.7, 0.4, 0.0, 0.0, 0.0, 0.4, 0.7],
    [0.0, 0.0, 0.0, 0.4, 0.7, 1.0, 0.7, 1.0, 0.7, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.7, 1.0, 0.7, 1.0, 0.7, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.7, 1.0, 0.7, 1.0, 0.7, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.7, 1.0, 0.7, 1.0, 0.7, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4],
    [0.0, 0.0, 0.0, 0.0, 0.4, 0.7, 1.0, 0.7, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.7, 1.0, 0.7, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.7, 1.0, 0.7, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.7, 1.0, 0.7, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
]

def fake_commits(
    commit_amount=1,
    commit_date=datetime.datetime(2024, 1, 7, tzinfo=datetime.timezone.utc),
):
    repo = Repo(".")
    mock_file = Path("commit_mocker.txt")
    for i in range(commit_amount):
        print(f"Mock commit {i} on {commit_date}")
        mock_file.write_text(f"Mock commit {i} on {commit_date}")
        repo.index.add(["commit_mocker.txt"])
        repo.index.add(["commit_mocker.txt"])
        os.system(f"git commit -m 'Mock commit {i}' --date='{commit_date}' --quiet")


def main():
    initial_pixel_matrix = np.array(PIXEL_MATRIX)
    pixel_matrix = initial_pixel_matrix.transpose()
    commit_date = datetime.datetime(2024, 1, 7)
    for column in pixel_matrix:
        for pixel in column:
            commit_amount = int(pixel * MULTIPLIER)
            print(f"Commit: {commit_amount}, Date: {commit_date}")
            fake_commits(commit_amount, commit_date)
            commit_date += datetime.timedelta(days=1)
        print()


if __name__ == "__main__":
    main()
    # how to execute command line in the terminal from the python code:



