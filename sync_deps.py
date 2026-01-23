# sync_deps.py
from tomlkit import parse, dumps
from tomlkit.items import Table

with open("requirements.txt") as f:
    deps = [
        line.strip()
        for line in f
        if line.strip() and not line.startswith("#")
    ]

with open("pyproject.toml") as f:
    data = parse(f.read())

project = data["project"]

if not isinstance(project, Table):
    raise TypeError("[project] section is missing or invalid")

project["dependencies"] = deps

with open("pyproject.toml", "w") as f:
    f.write(dumps(data))
