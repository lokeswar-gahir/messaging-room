#from socket import gethostname, gethostbyname
from uuid import uuid4

def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    # print('x_forwarded_for:', x_forwarded_for)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    # ip = request.META.get('REMOTE_ADDR')
    return ip.split(':')[0]

def get_or_create_device_id(request):
    device_id = request.COOKIES.get("device_id")
    if device_id:
        return device_id, False  # existing device
    return str(uuid4()), True  # new device

def add_new_ip_address_and_device_id(current_ip_and_device_id, new_ip, new_device):
    ip_device_combined = current_ip_and_device_id.split('|')
    ip_list = ip_device_combined[0]
    device_list = ip_device_combined[-1]

    ip_list = ip_list + ',' + new_ip
    device_list = device_list + ',' + new_device

    formatted_ip_and_device_id = ip_list + '|' + device_list
    return formatted_ip_and_device_id

# if __name__ == '__main__':
    # print(add_new_ip_address_and_device_id('some_ip|some_devide_id', 'new_ip', 'new_device_id'))
    # print(len('976785b3-5cd3-4870-87c9-9375661fcd25'))