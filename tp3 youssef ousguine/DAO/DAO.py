from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship

class PlayerEntity(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    game_id = Column(Integer, ForeignKey("game.id"), nullable=False)
    game = relationship("GameEntity", back_populates="players")
    battle_field = relationship("BattlefieldEntity", back_populates="player", uselist=False, cascade="all, delete-orphan")

class GameEntity(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    players = relationship("PlayerEntity", back_populates="game", cascade="all, delete-orphan")

class BattlefieldEntity(Base):
    __tablename__ = 'battlefield'
    id = Column(Integer, primary_key=True)
    min_x = Column(Integer, nullable=False)
    min_y = Column(Integer, nullable=False)
    min_z = Column(Integer, nullable=False)
    max_x = Column(Integer, nullable=False)
    max_y = Column(Integer, nullable=False)
    max_z = Column(Integer, nullable=False)
    max_power = Column(Integer, nullable=False)
    player_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    player = relationship("PlayerEntity", back_populates="battle_field")
    vessels = relationship("VesselEntity", back_populates="battlefield", cascade="all, delete-orphan")

class VesselEntity(Base):
    __tablename__ = 'vessel'
    id = Column(Integer, primary_key=True)
    coord_x = Column(Integer, nullable=False)
    coord_y = Column(Integer, nullable=False)
    coord_z = Column(Integer, nullable=False)
    hits_to_be_destroyed = Column(Integer, nullable=False)
    type = Column(Enum("Cruiser", "Destroyer", "Frigate", "Submarine", name="vessel_type"), nullable=False)
    battle_field_id = Column(Integer, ForeignKey("battlefield.id"), nullable=False)
    battlefield = relationship("BattlefieldEntity", back_populates="vessels")
    weapon = relationship("WeaponEntity", uselist=False, cascade="all, delete-orphan")

class WeaponEntity(Base):
    __tablename__ = 'weapon'
    id = Column(Integer, primary_key=True)
    ammunitions = Column(Integer, nullable=False)
    range = Column(Integer, nullable=False)
    type = Column(Enum("AirMissileLauncher", "SurfaceMissileLauncher", "TorpedoLauncher", name="weapon_type"), nullable=False)
    vessel_id = Column(Integer, ForeignKey("vessel.id"), nullable=False)
    vessel = relationship("VesselEntity", back_populates="weapon")

def map_to_game_entity(game: Game) -> GameEntity:
    game_entity = GameEntity()
    game_entity.id = game.id
    game_entity.players = [map_to_player_entity(player) for player in game.players]
    return game_entity

def map_to_game(game_entity: GameEntity) -> Game:
    game = Game(id=game_entity.id)
    game.players = [map_to_player(player_entity) for player_entity in game_entity.players]
    return game

def map_to_player_entity(player: Player) -> PlayerEntity:
    player_entity = PlayerEntity()
    player_entity.id = player.id
    player_entity.name = player.name
    player_entity.game_id = player.game_id
    player_entity.battle_field = map_to_battlefield_entity(player.battle_field, player_entity.id)
    return player_entity

def map_to_player(player_entity: PlayerEntity) -> Player:
    player = Player(id=player_entity.id, name=player_entity.name, game_id=player_entity.game_id)
    player.battle_field = map_to_battlefield(player_entity.battle_field)
    return player

def map_to_vessel_entity(vessel: Vessel, battlefield_id: int) -> VesselEntity:
    vessel_entity = VesselEntity()
    vessel_entity.id = vessel.id
    vessel_entity.coord_x = vessel.coordinates[0]
    vessel_entity.coord_y = vessel.coordinates[1]
    vessel_entity.coord_z = vessel.coordinates[2]
    vessel_entity.hits_to_be_destroyed = vessel.max_hits
    vessel_entity.type = vessel.type
    vessel_entity.battlefield_id = battlefield_id
    vessel_entity.weapon = map_to_weapon_entity(vessel.weapon, vessel_entity.id)
    return vessel_entity

def map_to_vessel(vessel_entity: VesselEntity) -> Vessel:
    vessel = Vessel(id=vessel_entity.id, coordinates=(vessel_entity.coord_x, vessel_entity.coord_y, vessel_entity.coord_z), max_hits=vessel_entity.hits_to_be_destroyed, type=vessel_entity.type)
    vessel.weapon = map_to_weapon(vessel_entity.weapon)
    return vessel

def map_to_weapon_entity(weapon: Weapon, vessel_id: int) -> WeaponEntity:
    weapon_entity = WeaponEntity()
    weapon_entity.id = weapon.id
    weapon_entity.ammunitions = weapon.ammunitions
    weapon_entity.range = weapon.range
    weapon_entity.type = weapon.type
    weapon_entity.vessel_id = vessel_id
    return weapon_entity

def map_to_weapon(weapon_entity: WeaponEntity) -> Weapon:
    weapon = Weapon(id=weapon_entity.id, ammunitions=weapon_entity.ammunitions, range=weapon_entity.range, type=weapon_entity.type)
    return weapon

def map_to_battlefield_entity(battlefield: Battlefield, player_id: int) -> BattlefieldEntity:
    battlefield_entity = BattlefieldEntity()
    battlefield_entity.id = battlefield.id
    battlefield_entity.min_x = battlefield.coordinates[0][0]
    battlefield_entity.min_y = battlefield.coordinates[0][1]
    battlefield_entity.min_z = battlefield.coordinates[0][2]
    battlefield_entity.max_x = battlefield.coordinates[1][0]
    battlefield_entity.max_y = battlefield.coordinates[1][1]
    battlefield_entity.max_z = battlefield.coordinates[1][2]
    battlefield_entity.max_power = battlefield.max_hits
    battlefield_entity.player_id = player_id
    return battlefield_entity

def map_to_battlefield(battlefield_entity: BattlefieldEntity) -> Battlefield:
    coordinates = [(battlefield_entity.min_x, battlefield_entity.min_y, battlefield_entity.min_z), (battlefield_entity.max_x, battlefield_entity.max_y, battlefield_entity.max_z)]
    battlefield = Battlefield(id=battlefield_entity.id, coordinates=coordinates, max_hits=battlefield_entity.max_power)
    return battlefield

