



from pydantic import BaseModel

class RegisterServiceDTO(BaseModel):
    
    username : str
    email : str
    password : str
    ip : str
    
