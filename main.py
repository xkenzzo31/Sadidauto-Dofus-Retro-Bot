from bot import Bot
from cmd_line_parser import Parser


def main():

    parser = Parser()
    args = parser.parse_command_line()
    bot = Bot(script=args.script,
              character_name=args.character_name,
              official_version=args.official_version,
              debug_window=args.debug_window)
    bot.Bot_Thread_start()


if __name__ == '__main__':
    main()
