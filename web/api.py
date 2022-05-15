from flask import Blueprint, jsonify, request
from server import game, data

blueprint = Blueprint(
    'api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/rez', methods=['GET'])
def get_rez():
    # чтобы это работало в части Ульяны в методе get_score класса Game я заменил
    # "return '\n'.join(w)" на "return w"
    try:
        sl = {}
        for i in game.get_score():
            team_name, score = i.split(' : ')
            sl[team_name] = int(score)
        return jsonify(sl)
    except Exception:
        return jsonify({'error': 'Empty request'})


@blueprint.route('/api/teamname/<int:user_id>', methods=['GET'])
def get_team_name(user_id):
    sl = {'team_name': data.get_team_name(user_id)}
    if sl['team_name'] is None:
        return jsonify({'error': 'Empty request'})
    return jsonify(sl)


@blueprint.route('/api/nick/<int:user_id>', methods=['GET'])
def get_nick(user_id):
    sl = {'nick': data.get_nick(user_id)}
    if sl['nick'] is None:
        return jsonify({'error': 'Empty request'})
    return jsonify(sl)


@blueprint.route('/api/avatar/<int:user_id>', methods=['GET'])
def get_avatar(user_id):
    sl = {'avatar': data.get_avatar(user_id)}
    if sl['avatar'] is None:
        return jsonify({'error': 'Empty request'})
    return jsonify(sl)


@blueprint.route('/api/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    sl = {'profile': data.get_profile(user_id)}
    if sl['profile'] is None:
        return jsonify({'error': 'Empty request'})
    return jsonify(sl)


@blueprint.route('/api/teamname/<int:user_id>', methods=['PUT'])
def set_team_name(user_id):
    try:
        team_name = get_team_name(user_id)
        for i in game.crews.keys():
            if i == team_name:
                game.crews[i].name = request.json['team_name']
        pr = data.set_team_name(user_id, request.json['team_name'])
        return jsonify({'status': 'OK' if pr else 'NO'})
    except Exception:
        return jsonify({'error': 'Empty request'})


@blueprint.route('/api/nick/<int:user_id>', methods=['PUT'])
def set_nick(user_id):
    try:
        pr = data.set_nick(user_id, request.json['nick'])
        return jsonify({'status': 'OK' if pr else 'NO'})
    except Exception:
        return jsonify({'error': 'Empty request'})


@blueprint.route('/api/avatar/<int:user_id>', methods=['PUT'])
def set_avatar(user_id):
    try:
        pr = data.set_avatar(user_id, request.json['avatar'])
        return jsonify({'status': 'OK' if pr else 'NO'})
    except Exception:
        return jsonify({'error': 'Empty request'})


@blueprint.route('/api/create/profile', methods=['POST'])
def create_profile():
    try:
        if not all(key in request.json for key in ['user_id', 'nick', 'team_name', 'avatar']):
            return jsonify({'error': 'Bad request'})
        if not all(isinstance(request.json[key], str) for key in ['nick', 'team_name']) and \
                not isinstance(request.json['user_id'], int) and not (isinstance(request.json['avatar'], str) or
                                                                      request.json['avatar'] is None):
            return jsonify({'error': 'Bad request'})
        pr = data.create_profile(request.json['user_id'], request.json['nick'], request.json['team_name'],
                                 request.json['avatar'])
        return jsonify({'status': 'OK' if pr else 'NO'})
    except Exception as ex:
        return jsonify({'error': ex})
