import dustpath


def main():
    app = dustpath.create_app()

    app.run(
            debug=True,
    )
