def insert_commas(x, *args):
    '''
    숫자의 천 단위마다 콤마를 찍어주는 formatter
    '''
    return "{:,.0f}".format(x)
