from threading import Event
active_session = {}

def create_session(key):
    active_session[key] = {
        "thread":None,
        "stop_event":Event(),
        "key":key
    }
    return active_session[key]

def stop_session(session_id):
    session = active_session.get(session_id,None)
    if session:
        session["stop_event"].set()
        return True
    return False

def get_session(session_id:str):
    return active_session[session_id]

def delete_session(session_id:str):
    return active_session.pop(session_id,None)

