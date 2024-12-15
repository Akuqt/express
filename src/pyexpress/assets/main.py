class HTML_PAGES:
    def __init__(self):
        pass

    def __template(self, content: str):
        return f"""                 <!DOCTYPE html>
                                    <html lang="en">
                                    <head>
                                        <meta charset="UTF-8">
                                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                        <title>Express.py</title>
                                    </head>
                                    <body>
                                        {content}
                                    </body>
                                    </html>
                                """

    def page_404(self, path: str):
        ret: str = f"""
                        <h1>404 - Page not found</h1>
                        <h5>Path: {path} was not found</h1>
                    """

        return f"""
                    {self.__template(ret)}
                """
