
# Get Julian Date from Gregorian
# fhr is a day time in Hours (e.g. "12.0" for 12:00:00 or #12.5" for 12:30:00)
def juldat(yr,mon,day,fhr):

    a=(14-mon)//12
    y=yr+4800-a
    m=mon+12*a-3

    juldat_right= day + (153*m+2)//5 + 365*y + y//4 - y//100 +y//400 -32045
    jd_right=fhr/24.0-0.5

    if jd_right>=1.0 :
        juldat_right+=1
        jd_right-=1.0
    if jd_right<0.0 :
        juldat_right-=1
        jd_right+=1.

    return [juldat_right,jd_right]# returns list of intrger and fractional parts
    # e.g. [ 2457600.0 , 0.5 ]


# Get Gregorian date from Julian (see format above)
def gregdat(jd1,jd2):

    fhr=jd2+0.5
    if fhr>=1.:
        jd1+=1
        fhr-=1.0
    
    a=jd1+32044
    b=(4*a+3)//146097
    c=a-(146097*b)//4
    d=(4*c+3)//1461
    e=c-(1461*d)//4
    m=(5*e+2)//153
    
    day=e-(153*m+2)//5+1
    mon=m+3-12*(m//10)
    yr=100*b+d-4800+m//10

    return [yr,mon,day,fhr*24.0]
    # list for Gregorian date
