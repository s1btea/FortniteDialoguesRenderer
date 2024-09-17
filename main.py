import os
from fdrenderer import VideoProcess, DataParser


def main():
    # Читаем данные.
    parser = DataParser("drops.json")
    data = parser.read()
    if data is None:
        input("Нажмите пробел, чтобы закрыть окно. > ")
        exit()

    # Создаём папку для кэша.
    # Там будут находится кадры для будущего видео.
    if not os.path.exists("cache"):
        os.makedirs("cache")
    
    # Обрабатываем все данные и создаём видео :)
    processor = VideoProcess(
        data,
        "./assets/inter-extra-bold.otf",
        (776, 200),
        "./assets/videos_fortnite.png",
        "result.mp4",
    )
    # ????
    processor.process_video()
    # PROFIT!!!11!!

if __name__ == "__main__":
    main()