import sys
import os
import shutil
local_dir = str(sys.argv[1])

bli_info = dict()

for p_dir in os.listdir(local_dir):
    p_path = os.path.join(local_dir, p_dir)
    if os.path.isdir(p_path) and p_dir != 'source':
        bli_info[p_dir] = dict()
        bli_info[p_dir]['video'] = []

        for video_dir in os.listdir(p_path):
            video_dir_path = os.path.join(p_path, video_dir)

            if os.path.isdir(video_dir_path):
                for video in os.listdir(video_dir_path):
                    video_path = os.path.join(video_dir_path, video)
                    if not os.path.isdir(video_path) and (
                            video.split('.')[-1] == 'flv' or video.split('.')[-1][0] == 'blv'):
                        bli_info[p_dir]['video'].append(video_path)

            elif video_dir == 'danmaku.xml':
                bli_info[p_dir]['danmaku'] = video_dir_path

for part in bli_info:
    part_path = os.path.join(local_dir, part)
    with open('ff.txt', 'w') as f:
        for line in bli_info[part]['video']:
            ff_line = "file '%s'" % line.strip() + '\n'
            f.write(ff_line)
    command = 'ffmpeg -f concat -safe 0 -i ff.txt -c copy %s.mp4' % part_path
    print(command)
    os.system(command=command)
    try:
        shutil.copy(bli_info[part]['danmaku'], part_path + '.xml')
    except KeyError:
        print('弹幕文件不存在...\n')

    shutil.move(part_path, os.path.join(os.path.join(local_dir, 'source'), part))

wait = input('完成！任意键退出')

