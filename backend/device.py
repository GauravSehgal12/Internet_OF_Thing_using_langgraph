DEFAULT_DEVICE_STATUS = {

    "Bedroom Light": "OFF",

    "Kitchen Light": "OFF",

    "Living Room Light": "OFF",

    "Fan": "OFF",

    "AC": "OFF",

    "Door": "Locked"
}


DEVICE_STATUS = DEFAULT_DEVICE_STATUS.copy()


def get_devices():
    return DEVICE_STATUS


def get_device_status(device):
    return DEVICE_STATUS.get(device)


def update_device(device, status):
    DEVICE_STATUS[device] = status


def reset_devices():
    global DEVICE_STATUS
    DEVICE_STATUS = DEFAULT_DEVICE_STATUS.copy()