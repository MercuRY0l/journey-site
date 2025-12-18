



from pydantic import BaseModel

class RegisterDTO(BaseModel):
    
    username : str
    email : str
    password : str
    password_repeat : str
    
