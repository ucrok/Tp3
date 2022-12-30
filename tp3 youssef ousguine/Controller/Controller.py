@app.post("/join-game")
async def join_game(game_data: JoinGameData) -> bool:
    return game_service.join_game(game_data.game_id, game_data.player_name)

@app.post("/add-vessel")
async def add_vessel(game_data: AddVesselData) -> bool:
    return game_service.add_vessel(game_data.game_id, game_data.player_name, game_data.vessel_type, game_data.x, game_data.y, game_data.z)

@app.post("/shoot-at")
async def shoot_at(game_data: ShootAtData) -> bool:
    return game_service.shoot_at(game_data.game_id, game_data.shooter_name, game_data.vessel_id, game_data.x, game_data.y, game_data.z)

@app.get("/game-status")
async def get_game_status(game_id: int, player_name: str) -> str:
    return game_service.get_game_status(game_id, player_name)

class JoinGameData(BaseModel):
    game_id: int
    player_name: str

class AddVesselData(BaseModel):
    game_id: int
    player_name: str
    vessel_type: str
    x: int
    y: int
    z: int

class ShootAtData(BaseModel):
    game_id: int
    shooter_name: str
    vessel_id: int
    x: int
    y: int
    z: int