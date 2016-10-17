#!/usr/bin/python2

from __future__ import division

import pyudev
import pygame

import sys
from collections import defaultdict
from functools import partial

watched_paths = {}
missing_devices = set()
screen_white = False
commands = {}
command_indices = defaultdict(int)

def device_description(device):
    try:
        product = device.attributes.asstring('product')
    except:
        product = None
    try:
        manufacturer = device.attributes.asstring('manufacturer')
    except:
        manufacturer = None
    if product and manufacturer:
        return '%s (%s)' % (product, manufacturer)
    elif manufacturer:
        return '%s device' % manufacturer
    elif product:
        return product
    else:
        return 'unknown device'

def exit():
    sys.exit(0)

def reset():
    global watched_paths
    global missing_devices
    print('Connected USB devices:')
    watched_paths = {}
    for device in context.list_devices(subsystem='usb', DEVTYPE='usb_device'):
        path = device.sys_path
        print('  %-60s  %s' % (path, device_description(device)))
        watched_paths[path] = device_description(device)
    missing_devices = set()

def handle_key(char):
    global commands
    global command_indices
    for command in commands:
        index = command_indices[command]
        if char == command[index]:
            index += 1
            if index == len(command):
                commands[command]()
                index = 0
        else:
            index = 0
        command_indices[command] = index

commands[u'exit'] = exit
commands[u'reset'] = reset

pygame.mixer.pre_init(44100, -16, 2)
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# screen = pygame.display.set_mode((640, 480))
alarm_sound = pygame.mixer.Sound('alarm.wav')
font = pygame.font.SysFont('Arial', 24)
pygame.mouse.set_visible(False)
white = (255, 255, 255)
black = (0, 0, 0)

context = pyudev.Context()
reset()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb')
monitor.start()

while True:
    for device in iter(partial(monitor.poll, 0.25), None):
        path = device.sys_path
        if path not in watched_paths:
            continue
        if device.action in ['remove', 'offline']:
            print('ALARM: %s REMOVED' % watched_paths[path])
            if not missing_devices:
                alarm_sound.play(-1)
            missing_devices.add(path)
        elif device.action in ['add', 'online']:
            print('ALARM END: %s ADDED' % watched_paths[path])
            missing_devices.remove(path)
            if not missing_devices:
                alarm_sound.stop()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # exit()
            pass
        elif event.type == pygame.KEYDOWN and event.unicode:
            handle_key(event.unicode)

    if missing_devices:
        screen_white = not screen_white
        screen.fill(white if screen_white else black)
        message = ', '.join(watched_paths[d] for d in missing_devices)
        text = font.render(message, True, black if screen_white else white)
        screen.blit(text, ((screen.get_width() - text.get_width()) // 2, (screen.get_height() - text.get_height()) // 2))
    else:
        screen_white = False
        screen.fill(black)
    pygame.display.flip()
