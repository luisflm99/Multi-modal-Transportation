class NotSolvable(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("El modelo no tiene solución, no se proporcionará ninguna solución", *args[1:])