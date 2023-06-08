from src import Express, Response, Request


def get(req: Request, res: Response):
    # print(req.headers)
    res.json({
        "Hello": "World!"
    })


app = Express()

app.get("/", get)

app.listen(cb=lambda h, p: print(f"http://{h}:{p}"))
