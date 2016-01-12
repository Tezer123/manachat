
import net.mapserv as mapserv
from utils import register_extension
import commands
import cui
import textutils
from loggers import debuglog


def being_chat(data):
    id_, message = data.id, data.message
    nick = mapserv.beings_cache[id_].name
    message = textutils.preprocess(message)
    m = "{} : {}".format(nick, message)
    debuglog.info(m)


def player_chat(data):
    message = textutils.preprocess(data.message)
    debuglog.info(message)


def got_whisper(data):
    nick, message = data.nick, data.message
    message = textutils.preprocess(message)
    m = "[{} ->] {}".format(nick, message)
    debuglog.info(m)


def send_whisper_result(data):
    if data.code == 0:
        message = textutils.preprocess(commands.whisper_msg)
        m = "[-> {}] {}".format(commands.whisper_to, message)
        debuglog.info(m)
        cui.input_win.clear()
        cui.input_win.addstr('/w "{}" '.format(commands.whisper_to))
        cui.input_win.refresh()
    else:
        debuglog.info("[error] {} is offline.".format(commands.whisper_to))


def party_chat(data):
    nick = mapserv.party_members.get(data.id, str(data.id))
    message = textutils.preprocess(data.message)
    m = "[Party] {} : {}".format(nick, message)
    debuglog.info(m)


def player_warp(data):
    mapserv.cmsg_map_loaded()


def map_login_success(data):
    mapserv.cmsg_map_loaded()


def connection_problem(data):
    error_codes = {
        2 : "Account already in use"
    }
    msg = error_codes.get(data.code, str(data.code))
    debuglog.error('Connection problem: %s', msg)


def register_all():
    register_extension("smsg_being_chat", being_chat)
    register_extension("smsg_player_chat", player_chat)
    register_extension("smsg_whisper", got_whisper)
    register_extension("smsg_whisper_response", send_whisper_result)
    register_extension("smsg_party_chat", party_chat)
    register_extension("smsg_player_warp", player_warp)
    register_extension("smsg_map_login_success", map_login_success)
    register_extension("smsg_connection_problem", connection_problem)
