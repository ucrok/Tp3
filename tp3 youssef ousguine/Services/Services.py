def join_game(self, game_id: int, player_name: str) -> bool:
    game = self.game_dao.find_game(game_id)
    if not game:
        return False
    other_player = game.players[0]
    battle_field = other_player.battle_field
    new_player = Player(player_name, battle_field)
    game.add_player(new_player)
    self.game_dao.update_game(game)
    return True

def get_game(self, game_id: int) -> Game:
    return self.game_dao.find_game(game_id)

def add_vessel(self, game_id: int, player_name: str, vessel_type: str, x: int, y: int, z: int) -> bool:
    game = self.game_dao.find_game(game_id)
    player = game.get_player(player_name)
    if player:
        vessel = Vessel(vessel_type, x, y, z)
        player.add_vessel(vessel)
        self.game_dao.update_player(player)
        return True
    else:
        return False

def shoot_at(self, game_id: int, shooter_name: str, vessel_id: int, x: int, y: int, z: int) -> bool:
    game = self.game_dao.find_game(game_id)
    shooter = game.get_player(shooter_name)
    if shooter:
        vessel = shooter.get_vessel(vessel_id)
        if vessel:
            if vessel.shoot_at(x, y, z):
                self.game_dao.update_player(shooter)
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def get_game_status(self, game_id: int, shooter_name: int) -> str:
    game = self.game_dao.find_game(game_id)
    shooter = game.get_player(shooter_name)
    if shooter.has_won():
        return "GAGNE"
    elif shooter.has_lost():
        return "PERDU"
    else:
        return "ENCOURS"
