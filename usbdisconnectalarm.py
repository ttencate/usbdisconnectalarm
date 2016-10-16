#!/usr/bin/python2

import pyudev

def device_description(device):
    try:
        product = device.attributes.asstring('product')
    except:
        product = 'unknown product'
    try:
        manufacturer = device.attributes.asstring('manufacturer')
    except:
        manufacturer = 'unknown manufacturer'
    return '%s (%s)' % (product, manufacturer)

context = pyudev.Context()

print('detecting devices')

watched_paths = {}
for device in context.list_devices(subsystem='usb', DEVTYPE='usb_device'):
    path = device.sys_path
    print('%-60s  %s' % (path, device_description(device)))
    watched_paths[path] = device_description(device)

print('starting monitor')

monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb')

for device in iter(monitor.poll, None):
    path = device.sys_path
    if path not in watched_paths:
        continue
    if device.action in ['remove', 'offline']:
        print('ALARM: %s REMOVED' % watched_paths[path])
    elif device.action in ['add', 'online']:
        print('ALARM END: %s ADDED' % watched_paths[path])
