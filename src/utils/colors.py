class Colors:
    @classmethod
    def colored(__class__, text, color):
        return f"{getattr(__class__, color)}{text}{__class__.ENDC}"

    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    