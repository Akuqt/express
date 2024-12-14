from src import Express, Response, Request, Router


def get(req: Request, res: Response):
    res.json({"Hello": "World!"})


def get_test(req: Request, res: Response):
    res.json({"test": "Hello World!"})


def middleware1(req: Request, res: Response, next):
    res.add_header("X-Test-1", "Middleware")
    next()


def middleware2(req: Request, res: Response, next):
    res.add_header("X-Test-2", "Middleware")
    next()


router = Router()

router.get("/test/a", middleware1, middleware2, get_test)

app = Express()

app.use(router)

app.get("/", None, get)

app.listen(cb=lambda h, p: print(f"http://{h}:{p}"))
