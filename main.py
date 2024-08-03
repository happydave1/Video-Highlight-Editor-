import os, platform

# SET IMAGEMAGICK ENVIRONMENT VARIABLE TO RAW STRING POINTING TO PROGRAM
if platform.system() == 'Windows':
  print('im running on windows!')
  os.environ["IMAGEMAGICK_BINARY"] = R"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
elif platform.system() == 'Linux':
  # running on docker container
  print(os.environ.get("IMAGEMAGICK_BINARY"))


from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip

def parse_time_stamp_into_seconds(time_stamp):
  # NOTE time_stamp will be given in a format "MINUTES:SECONDS"
  minutes = ""
  counter = 0
  for index, digit in enumerate(time_stamp):
    if digit != ':':
      minutes += digit
      counter = index
    else:
      break
  
  seconds = time_stamp[counter + 2:]

  minutes = int(minutes)
  seconds = int(seconds)

  return (minutes * 60) + seconds

def check_if_video_exists(video):
  # CHECKS THE 'highlights' folder if a video exists
  full_video_path = os.path.join('highlights', video)
  return os.path.isfile(full_video_path)

def create_highlight_reel(video, highlights, output, colorOfFont):

  og_video = VideoFileClip(os.path.join('highlights', video))

  highlight_clips_array = []

  for highlight in highlights:

    start_time = parse_time_stamp_into_seconds(highlight[0])

    end_time = parse_time_stamp_into_seconds(highlight[1])

    highlight_description = highlight[2]

    curr_clip = og_video.subclip(start_time, end_time)
    text_clip = TextClip(highlight_description, fontsize=65, color=f"{colorOfFont}", font="Bodoni-MT")
    text_clip = text_clip.set_duration(curr_clip.duration)
    text_clip = text_clip.set_position(("left", "bottom"))

    highlight_clip = CompositeVideoClip([curr_clip, text_clip])
    highlight_clips_array.append(highlight_clip)

  final_reel = concatenate_videoclips(highlight_clips_array)

  final_reel.write_videofile(output, codec="libx264")

# a function which goes through the folder outputs and stitches together
# every video from outputs
def make_final_reel(path_to_outputs_folder, path_to_final_reel_output):
  clip_array = []

  # Go through the folder and append every video clip to the array
  for filename in sorted(os.listdir(path_to_outputs_folder)):
      if filename.endswith(".mp4"):  # Adjust this if your videos have a different extension
          filepath = os.path.join(path_to_outputs_folder, filename)
          clip = VideoFileClip(filepath)
          clip_array.append(clip)

  # use concatenate_videoclips to create a final clip
  final_clip = concatenate_videoclips(clip_array)

  # write to outputs folder
  final_clip.write_videofile(path_to_final_reel_output)

# video_name = "IMG_6706.MOV"
# colorOfFont = "Black"
# description_prefix = "Samuel Zhao - Number 13 -"
# video = f"highlights/{video_name}"
# output = f"outputs/finished{video_name}.mp4"
# highlights = [
#     (90, 97, f"{description_prefix} Drive into Layup"),
# ]

def main():

  # prompt user for arguments for highlights
  highlight_or_final_clip = input("Thanks for using my Highlight Editor! Do you want to make a highlight or a final video?\n").strip().lower()

  print(f"you selected: {highlight_or_final_clip}")

  if highlight_or_final_clip == 'highlight':
    video_name = input("Enter the full filename (extension included) of the video you want to splice. Please note that it must be in the highlights folder.\n").strip()

    is_valid_video = check_if_video_exists(video_name)
    if not is_valid_video:
      print('not a valid video, please try again')
      return
    print('video exists in highlights folder!')

    font_color = input("Enter the color of the font you would like to use in the video.\n").capitalize()

    # if b'{font_color}' not in TextClip.list('font'):
    #   print('color not available')
    #   return
    
    print(f'you selected {font_color}. Valid font color')

    description_prefix = input("Enter the description prefix you want on the lower left.\n")

    print(f"you want {description_prefix} on the bottom left")

    highlights = []

    continue_entering_highlights = 'Y'
    while continue_entering_highlights == 'Y':
      highlight_start_time = input("input highlight start time in MINUTES:SECONDS format\n")
      highlight_end_time = input("input highlight end time.\n")
      highlight_description = input("input highlight description\n")
      full_highlight_description = f'{description_prefix} {highlight_description}'
      confirm_highlight = input(f"your highlight will begin at {highlight_start_time}, end at {highlight_end_time}. Description will be: {full_highlight_description}. Is this good? (Y/N)\n").upper()
      if confirm_highlight == 'N':
        print("retry")
        return
      continue_entering_highlights = input("continue entering highlights? (Y/N)\n").strip().upper()
      highlights.append((highlight_start_time, highlight_end_time, full_highlight_description))

    print(f"creating highlight reel of {len(highlights)} clips.")
    # execute function call
    create_highlight_reel(video_name, highlights, f"outputs/finished{video_name}.mp4", font_color)

  elif highlight_or_final_clip == 'final video':
    final_video_name = input("ok, the final video will go through the outputs folder and appened every clip together. What do you want the final video name to be? (Include file extension) \n")
    print(f"Creating final video. Available at {os.path.join('outputs', 'final_videos', final_video_name)}")
    make_final_reel('outputs', os.path.join('outputs', 'final_videos', final_video_name))


if __name__ == "__main__":
  # create highlight reel for given video
  # create_highlight_reel(video, highlights, output, colorOfFont)

  main()
  

# CREATING FINAL REEL:
# make_final_reel("outputs", "finalreels/finalreel1.mp4")