from config import GAME_CFG


def collides(left_obj, right_obj):
    if left_obj.x < right_obj.x + GAME_CFG.FIELD_SIZE and left_obj.x + GAME_CFG.FIELD_SIZE > right_obj.x \
            and left_obj.y < right_obj.y + GAME_CFG.FIELD_SIZE and left_obj.y + GAME_CFG.FIELD_SIZE > right_obj.y:
        return True
    return False
