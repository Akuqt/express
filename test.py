from src import Express, Response, Request, Router


def get(req: Request, res: Response):
    res.json(
        [
            {
                "id": 1,
                "name": "Cathy Borer",
                "company": "Boyer and Sons",
                "username": "Macey42",
                "email": "Zackery.McKenzie92@hotmail.com",
                "address": "8996 Ruecker Extensions",
                "zip": "86714",
                "state": "Washington",
                "country": "Ukraine",
                "phone": "569.257.2774 x61895",
                "photo": "https://json-server.dev/ai-profiles/82.png",
            },
            {
                "id": 2,
                "name": "Cecil Faker",
                "company": "Kuhic - Abbott",
                "username": "Sabryna_Bechtelar60",
                "email": "Henry12@gmail.com",
                "address": "65230 E 4th Avenue",
                "zip": "86942-7603",
                "state": "Delaware",
                "country": "Guernsey",
                "phone": "287-671-1038",
                "photo": "https://json-server.dev/ai-profiles/54.png",
            },
        ]
    )


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
