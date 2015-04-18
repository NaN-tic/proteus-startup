from proteus import config, Model


User = Model.get('res.user')


def reload_context():
    config._context = User.get_preferences(True, config.context)
