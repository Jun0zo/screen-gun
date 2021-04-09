import re

src = '/usr/local/include/opencv4/opencv2/'
file_list_global = []




def edit_file(file_name, N):

    file_name = file_name.replace('>', '')
    file_name.replace('<', '')
    file_name.replace('\n', '')

    print('+++++++++++++ ' + file_name + ' +++++++++++++')
    global file_list_global
    header = open(src + file_name, 'r')

    file_list_inner = []

    while True:
        line = header.readline()

        if not line:
            break

        if "opencv2/" in line:
            line = line.replace('>', '"')
            line.replace('<', '"')
            add_point = line.find('opencv')
            print(line)

            puzzle = line.split('"')

            for index in puzzle:

                if 'opencv2' in index:
                    file_name = ''
                    puzzle_2 = index.split('/')

                    if len(puzzle_2) < 2:  # ???
                        print('Error 001 : no file !!!')
                        break

                    elif len(puzzle_2) == 2:  # /opencv/~.hpp
                        file_name = puzzle_2[1]

                    elif len(puzzle_2) > 2:  # /opencv/~/~/~ ... ~.hpp
                        file = ''

                        print(puzzle_2)
                        for i in range(1, len(puzzle_2)):
                            if file != '\n':
                                file += puzzle_2[i]
                            if 1 <= i < len(puzzle_2)-1:
                                file += '/'

                        file_name = file

                    flag = file_name in file_list_global
                    if flag is False:  # 처음 접근하는 헤더파일일 때
                        file_list_inner.append(file_name)
                        file_list_global.append(file_name)
                        print('===== ' * N, end='')

                    else:
                        print('xxxx ' * N, end='')

                    print(file_name)

    header.close()

    if not file_list_inner:
        return

    index = 2
    for item in file_list_inner:
        if item != False:
            edit_file(item, index)
        index += 1

if __name__ == '__main__':
    # edit_file('opencv.hpp', 1)
    edit_file('core.hpp', 1)