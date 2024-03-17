CMD = '/usr/local/bin/ffmpeg -i {input_file} -s {out_width}x{out_height} -profile:v high444 -c:v libx264 -preset veryslow -crf 30 -r 30 -g 120 -keyint_min 30 -sc_threshold 40 -bf 3 -b_strategy 2 -refs 5 -c:a libfdk_aac -profile:a aac_low -b:a 128k -movflags faststart -max_muxing_queue_size 9999 -f mp4 -loglevel error {out_file} -y'