D = {}

while True:
    print('1 : 검색\n2 : 추가\n3 : 종료')
    x = int(input('숫자를 입력하세요 : '))

    if x == 1:
        for a in D:
            print(a, end = ' ')
        print()
        k = input('종류를 입력하세요 : ')
        if k not in D:
            print('사전에 없는 종류입니다')
            continue
        
        n = input('이름을 입력하세요 : ')
        if n in D[k]:
            print('[%s] : [%s]\n%s' % (k, n, D[k][n]))
        else:
            print('아이템이 존재하지 않습니다. 먼저 추가해주세요')
    elif x == 2:
        k = input('종류를 입력하세요 : ')
        if k not in D:
            D[k] = {}
            
        n = input('이름을 입력하세요 : ')
        if n in D[k]:
            print('이미 존재하는 이름입니다')
            continue
        else:
            D[k][n] = input('설명을 추가하세요 : ')
    elif x == 3:
        break
    else:
        print('잘못된 숫자입니다 다시 입력해주세요')
        continue
