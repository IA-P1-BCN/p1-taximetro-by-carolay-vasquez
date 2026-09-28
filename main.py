from taximetro.cli import main
from taximetro.logging_config import configure_logging

if __name__ == "__main__":
    configure_logging()
    main()