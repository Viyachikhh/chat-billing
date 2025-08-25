from typing import Literal, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pydantic import BaseModel


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


class ErrorResponse(BaseModel):
    message: str


class SuccessResponse(BaseModel):
    message: str