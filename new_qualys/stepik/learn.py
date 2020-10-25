s = 'abcdefghijk'
def main():
    a = input()
    c = a[0]
    result = ''
    for i in a[1:]:
        s = 1
        if i == c:
            s += 1
        else:
            result += (i + str(s))
    print(result)


if __name__ == '__main__':
    print(main())
