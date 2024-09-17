from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

from .model import DropFile
from .image_process import ImageProcess


class VideoProcess:

    def __init__(
        self,
        data: dict[str, list[DropFile]],
        font_path: str,
        box_size: tuple[int, int],
        template_path: str,
        output_video_path: str,
    ) -> None:
        self.__data = data
        self.__font_path = font_path  # "./assets/inter-extra-bold.otf"
        self.__box_size = box_size  # (252, 250)
        self.__template_path = template_path  # "./assets/videos_fortnite.png"
        self.__output_video_path = output_video_path  # "result.mp4"

    def process_video(self):
        image_processor = ImageProcess(
            self.__font_path, self.__box_size, self.__template_path
        )
        clips = []
        for drops in self.__data.values():
            for drop in drops:
                audioFile = drop.AudiofilePath
                delay = drop.Delay
                subtitles = drop.Subtitles

                image = image_processor.process_image(subtitles)
                audio_сlip = AudioFileClip(audioFile)
                image_clip: ImageClip = (
                    ImageClip(image)
                    .set_duration(audio_сlip.duration + delay)
                    .set_audio(audio_сlip)
                )
                clips.append(image_clip)

        final_video = concatenate_videoclips(clips)
        final_video.write_videofile(self.__output_video_path, codec="libx264", fps=24)
