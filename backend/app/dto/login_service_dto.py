



from pydantic import BaseModel

class LoginServiceDTO(BaseModel):
    
    username: str
    password: str
    ip : str
        
