from typing import Literal, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict


@dataclass
class MessageDTO:
    role: Literal["system", "human"]
    text: str


@dataclass
class QuestionDTO:
    text: str
    history: list[MessageDTO]


@dataclass
class AnswerDTO:
    text: str
    used_tokens: int


class LLMService(ABC):

    @abstractmethod
    def execute(self, data: QuestionDTO) -> AnswerDTO:
        raise NotImplementedError
    

@dataclass
class UserDTO:
    id: str
    name: str
    username: str
    hashed_password: str


# User base schema
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
    

# Service base schema
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
    
class InMemoryUserRepository(UserRepository):
    
    def __init__(self):
        self.list_users = []
    
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