from collections.abc import Callable
from ..request import Request
from ..response import Response

type ReqResTuple = tuple[Request, Response]
type NextCallback = Callable[[None], None]
type Middleware = Callable[[Request, Response, NextCallback], None]
type Callback = Callable[[Request, Response], None]
