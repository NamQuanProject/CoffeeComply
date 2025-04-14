from dataclasses import dataclass, field
from typing import List

@dataclass
class SubTradeTopic:
    title: str
    url: str
    description: str
    summary: str



@dataclass
class MainTradeTopic:
    name: str
    url: str
    subtopics: List[SubTradeTopic] = field(default_factory=list)









