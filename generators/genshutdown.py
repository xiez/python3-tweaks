from tail import follow

lines = follow(open('www/access-log'))
for i, line in enumerate(lines):
    print(i, 'line: ', line, end='')
    if i == 4:
        lines.close()
