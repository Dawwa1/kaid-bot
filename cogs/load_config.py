import tomli

def openConfig():
    with open('config.toml', mode="rb") as fp:
        return tomli.load(fp) 