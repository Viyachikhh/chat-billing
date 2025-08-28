from passlib.context import CryptContext
from uuid import uuid4
from dataclasses import asdict
from typing import Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod

from src.api.general_schemas import * 

@dataclass
class UserDTO:
    id: str
    name: str
    username: str
    hashed_password: str


class UserRepository(ABC):

    @abstractmethod
    async def get_one(self, user_id: str) -> Optional[UserDTO]:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, **filters) -> list[UserDTO]:
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, data: UserDTO) -> UserDTO:
        raise NotImplementedError


class InMemoryUserRepository(UserRepository):
    instance = None
    list_users = []
    
    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance 
        
    def __init__(self):
        pass
    
    def get_one(self, user_id: str) -> Optional[UserDTO]:
        for user_dto in self.list_users:
            if user_dto.id == user_id:
                return user_dto
        return None

    def get_all(self, **filters) -> list[UserDTO]:
        if len(filters) == 0:
            return self.list_users
        else:
            result = []
            for user_dto in self.list_users:
                user_dto_dump = asdict(user_dto)
                necessary_fields = {f_key: user_dto_dump[f_key] for f_key in filters.keys()}
                if necessary_fields == filters:
                    result.append(user_dto)
            return result
                    
    def add_one(self, data: UserDTO) -> UserDTO:
        self.list_users.append(data)
        return data


class BaseAuthService(ABC):

    @abstractmethod
    async def login(self, username: str, password: str) -> Optional[UserDTO]:
        raise NotImplementedError

    @abstractmethod
    async def register(self, name: str, username: str, password: str) -> UserDTO:
        raise NotImplementedError
    
    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> Optional[UserDTO]:
        raise NotImplementedError


class AuthService(BaseAuthService):

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def login(self, username: str, password: str) -> Optional[UserDTO]:
        users = await self._user_repository.get_all(username=username)
        for user in users:
            if self._verify_password(password, user.hashed_password):
                return user
        return None

    async def register(self, name: str, username: str, password: str) -> UserDTO:
        user_id = str(uuid4())
        hashed_password = self._hash_password(password)
        user = UserDTO(id=user_id, name=name, username=username, hashed_password=hashed_password)
        await self._user_repository.add_one(user)
        return user

    async def get_user_by_id(self, user_id: str) -> Optional[UserDTO]:
        user = await self._user_repository.get_one(user_id)
        return user

    @staticmethod
    def _hash_password(password: str) -> str:
        ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = ctx.hash(password)
        return hashed_password

    @staticmethod
    def _verify_password(password: str, hashed_password: str) -> bool:
        ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
        is_verified = ctx.verify(password, hashed_password)
        return is_verified