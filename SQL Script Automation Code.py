# Fraser Isbester 2019

def parse_sql(filename):
    data = open(filename, 'r').readlines()
    stmts = []
    DELIMITER = ';'
    stmt = ''

    comment_flag = 0
    inquote_flag = 0

    for lineno, line in enumerate(data):

        quote_count = line.count("'")
        del_count = line.count(DELIMITER)

        # Handle Comment Blocks
        if('/*' in line and '*/' not in line and comment_flag != 1):
            # print("Found Comment start:", line)
            # input("")
            comment_flag = 1
            continue
        if('*/' in line and '/*' not in line and comment_flag != 0):
            # print("Found Comment end")
            # input("")
            comment_flag = 0
            continue
        if(comment_flag == 1 or line.startswith('--')):
            # print("Skipping:", line)
            # input("")
            continue
        # Handle Delimer-in-quote problems
        if(quote_count > 0 and del_count > 0):
            stmt_buffer = ''
            for char in line:
                if(char == "\\'"):
                    stmt_buffer += char
                elif(char == "'"):
                    inquote_flag += 1
                if(char == DELIMITER):
                    if(inquote_flag % 2 == 0):
                        stmt_buffer += char
                        stmt += stmt_buffer
                        stmts.append(stmt.strip())
                        stmt = ''
                        continue
                    elif(inquote_flag % 2 != 0):
                        stmt_buffer += char
                    else:
                        print("Big error in del-in-quote proccessing")
                        quit()
                else:
                    stmt_buffer += char
            stmt += stmt_buffer
            continue

        if not line.strip():
            continue

        if 'DELIMITER' in line:
            print('DELIMITER In line?')
            input("")
            DELIMITER = line.split()[1]
            continue

        if (DELIMITER not in line):
            stmt += line.replace(DELIMITER, ';')
            continue

        if stmt:
            stmt += line
            stmts.append(stmt.strip())
            stmt = ''
        else:
            stmts.append(line.strip())

    return stmts
