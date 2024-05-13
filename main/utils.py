from socket import gethostname, gethostbyname

def get_ip(request):
    # host = gethostname()
    # return gethostbyname(host)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    # ip = request.META.get('REMOTE_ADDR')
    return ip