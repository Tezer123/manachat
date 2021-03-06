import re
import random
import types
import net.mapserv as mapserv
from utils import extends


__all__ = [ 'PLUGIN', 'init', 'answer', 'commands' ]


PLUGIN = {
    'name': 'chatbot',
    'requires': (),
    'blocks': (),
}


def answer_info(nick, message, is_whisper, match):
    if is_whisper:
        mapserv.cmsg_chat_whisper(nick, "answer to !info")
    else:
        mapserv.cmsg_chat_message("You are too curious, {}".format(nick))


commands = {
    r'^!help' : ["What do you need help with?"],
    r'^!info' : answer_info
}


def answer_random(nick, message, is_whisper, answers):
    resp = random.choice(answers)
    if is_whisper:
        mapserv.cmsg_chat_whisper(nick, resp)
    else:
        mapserv.cmsg_chat_message(resp)


def answer(nick, message, is_whisper):
    for cmd, action in commands.iteritems():
        regex = re.compile(cmd)
        match = regex.match(message)
        if match:
            if isinstance(action, types.ListType):
                answer_random(nick, message, is_whisper, action)
            elif isinstance(action, types.FunctionType):
                action(nick, message, is_whisper, match)
            else:
                raise ValueError("must be either list or function")


@extends('smsg_being_chat')
def being_chat(data):
    id_, message = data.id, data.message
    nick = mapserv.beings_cache[id_].name
    answer(nick, message, False)


@extends('smsg_whisper')
def got_whisper(data):
    nick, message = data.nick, data.message
    answer(nick, message, True)


@extends('smsg_whisper_response')
def send_whisper_result(data):
    pass


def init(config):
    pass
