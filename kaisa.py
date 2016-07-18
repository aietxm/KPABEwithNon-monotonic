s='DISJV_Hej_UdShofjyed'
daxie =   'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
xiaoxie = 'abcdefghijklmnopqrstuvwsyz'
for i in range(26):
    str = ''
    for j in range(len(s)):
        c = ord(s[j])
        if c>=65 and c<=90:
            temp = daxie[((c-65)+i)%26]
        elif c>=97 and c<=122:
            temp = xiaoxie[((c-97)+i)%26]
        else:
            temp = chr(c)
        str = str+temp
    print str