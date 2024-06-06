import fontforge  # noqa
import os
import multiprocessing as mp
import argparse

def convert_mp(opts):
    """Using multiprocessing to convert all fonts to sfd files"""
    charset = open(opts.charset_path, 'r').read()
    charset_lenw = len(str(len(charset)))
    fonts_file_path = opts.ttf_path
    sfd_path = opts.sfd_path
    for root, dirs, files in os.walk(fonts_file_path):
        ttf_fnames = files
    
    font_num = len(ttf_fnames)
    process_num = min(opts.workers, mp.cpu_count() - 1)
    font_num_per_process = font_num // process_num + 1

    def process(process_id, font_num_p_process):
        for i in range(process_id * font_num_p_process, (process_id + 1) * font_num_p_process):
            if i >= font_num:
                break
            
            font_id = ttf_fnames[i].split('.')[0]
            font_name = ttf_fnames[i]
            
            font_file_path = os.path.join(fonts_file_path, font_name)
            try:
                cur_font = fontforge.open(font_file_path)
            except Exception as e:
                print('Cannot open ', font_name)
                print(e)
                continue

            target_dir = os.path.join(sfd_path, "{}".format(font_id))
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            for char_id, char in enumerate(charset):
                char_description = open(os.path.join(target_dir, '{}_{num:0{width}}.txt'.format(font_id, num=char_id, width=charset_lenw)), 'w')

                cur_font.selection.select(char)
                cur_font.copy()

                new_font_for_char = fontforge.font()
                char = 'A'
                new_font_for_char.selection.select(char)
                new_font_for_char.paste()
                new_font_for_char.fontname = "{}_".format(font_id) + font_name

                if opts.margin:
                    new_font_for_char[char].left_side_bearing = opts.margin
                    new_font_for_char[char].right_side_bearing = opts.margin

                new_font_for_char.save(os.path.join(target_dir, '{}_{num:0{width}}.sfd'.format(font_id, num=char_id, width=charset_lenw)))

                char_description.write(str(ord(char)) + '\n')
                char_description.write(str(new_font_for_char[char].width) + '\n')
                char_description.write(str(new_font_for_char[char].vwidth) + '\n')
                char_description.write('{num:0{width}}'.format(num=char_id, width=charset_lenw) + '\n')
                char_description.write('{}'.format(font_id))

                char_description.close()

            cur_font.close()

    processes = [mp.Process(target=process, args=(pid, font_num_per_process)) for pid in range(process_num)]

    for p in processes:
        p.start()
    for p in processes:
        p.join()

def main():
    parser = argparse.ArgumentParser(description="Convert ttf fonts to sfd fonts")
    parser.add_argument("--ttf_path", type=str, required=True, help='Path to TTF font files directory')
    parser.add_argument('--sfd_path', type=str, required=True, help='Path to save SFD font files')
    parser.add_argument('--charset_path', type=str, required=True, help='Path to charset.txt file')
    parser.add_argument('--workers', type=int, default=mp.cpu_count() - 1, help='Number of worker processes to use')
    parser.add_argument('--margin', type=int, default=0, help='Margin for character bounding box')
    opts = parser.parse_args()
    convert_mp(opts)

if __name__ == "__main__":
    main()