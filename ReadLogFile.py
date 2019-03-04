with open("/home/mintu/essentials/Smart Retail/logs/web-1/access.log.2" , 'r') as f:
    count = 0
    for line in f:
        if '/orders/ HTTP/1.1" 20' in line:
            bytes(line, 'utf-8').decode('string_escape')
            print (line)
