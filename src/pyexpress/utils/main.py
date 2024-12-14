from os import linesep
from re import findall
from urllib.parse import parse_qs


def __array2dict(array: list[bytes]) -> dict:
    res = {}
    for i in array:
        c = i.decode("utf-8").split(": ")
        if len(c) != 2:
            continue
        res[c[0].lower()] = c[1]
    return res


def parse_headers(raw: bytes) -> tuple[bytes, dict]:
    if len(raw.decode("utf-8")) == 0:
        return b"", {}
    data_ = raw.rsplit((linesep * 2).encode("utf-8"))
    if len(data_) < 2:
        data_.append(b"")
    data = data_[0].rsplit((linesep).encode("utf-8"))
    body = (linesep * 2).encode("utf-8") + data_[1]
    info = data.pop(0).decode("utf-8").split(" ")
    method = info.pop(0)
    route = info.pop(0)
    http_version = info.pop(0).split("/")[1]
    headers = __array2dict(data)
    headers["method"] = method
    headers["http-version"] = http_version
    headers["route"] = route
    return body, headers


def set_route_data(name: str, query: str):
    return {
        "name": name,
        "query": query,
    }


def get_route_data(path: str):
    res: dict[str, str | bool] = {}
    if path.find("?") != -1:
        content = path.split("?")
        if len(content) > 2:
            content = [content[0], "?".join(i for i in content[1::])]
        res = set_route_data(content[0], content[1])
    else:
        res = set_route_data(path, "")
    return res


def parse_route(route: str, headers: dict[str, str]):
    query: dict[str, dict[str, list[str]]] = {}
    route = add_slash(route)
    paths = add_slash(headers["route"]).split("/")
    normalized = ""
    for path in paths:
        if path == "":
            continue
        route_data = get_route_data(path)
        normalized += "/" + route_data["name"]
        query[route_data["name"]] = parse_qs(route_data["query"])

    return query, add_slash(normalized)


def add_slash(path: str):
    if not path.endswith("/"):
        path += "/"
    if not path.startswith("/"):
        path = f"/{path}"
    return path


def match_routes(real: str, defined: str):
    r = real.split("/")
    d = defined.split("/")
    if real == defined:
        return True
    if len(r) != len(d):
        return False
    params = get_params(real, defined)
    if len(params.keys()) == 0:
        return False
    final = defined
    for key in params.keys():
        final = final.replace(f":{key}", params[key])
    return final == real


def get_params(real: str, defined: str) -> dict[str, str]:
    rg = r"\:[a-zA-Z0-9]"
    params = findall(rg, defined)
    matcher = defined
    for item in params:
        matcher = matcher.replace(item, "(.*)")
    params_data = findall(matcher, real)
    if len(params_data) < 1:
        return {}
    data = params_data[0]
    if not type(data) is tuple:
        data = (data,)
    if len(data) != len(params):
        return {}
    final: dict[str, str] = {}
    for i in range(len(data)):
        final[params[i][1::]] = data[i]
    return final
