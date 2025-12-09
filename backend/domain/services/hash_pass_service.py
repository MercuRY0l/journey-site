




from domain.interfaces.hash_interface import IHashService
from argon2 import PasswordHasher
from argon2.low_level import Type
class HashService(IHashService):
    
    def __init__(self):
        self.ph = PasswordHasher(
        time_cost=3,
        memory_cost=64*1024, 
        parallelism=2,
        hash_len=32,
        salt_len=16,
        type=Type.ID       
    )
     
    def hash(self, object : str) -> str:
        return self.ph.hash(object)
    
    def check(self, plaintext: str, hashed: str) -> bool:
        try:
            return self.ph.verify(hashed, plaintext)
        except Exception:
            return False
        
    