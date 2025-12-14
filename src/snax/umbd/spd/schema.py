from dataclasses import dataclass
from enum import Enum
from typing import List


class Group(str, Enum):
    IDENTIFIER = "IDENTIFIER"
    DEMOGRAPHIC = "DEMOGRAPHIC"
    INTERESTS = "INTERESTS"
    PREFERENCE = "PREFERENCE"
    SELF_PERCEPTION = "SELF_PERCEPTION"


@dataclass(frozen=False)
class Col:
    name: str
    desc: str
    dtype: str
    tags: List[str] | None = None
    group: str | Group | None = None

    def __post_init__(self):
        self.tags = self.name.split("_") + self.desc.split(" ")


identifier_tags = ["id", "identifier", "key"]
demographic_tags = ["demographic", "demo"]
interest_tags = ["interest", "hobby", "preference"]
outcome_tags = ["outcome", "target", "label"]
what_you_seek_tags = ["seek", "preference"]
self_perception_tags = ["self", "self-perception"]
ratings_given_tags = ["rating", "given", "partner"]


class tags(Enum):
    IDENTIFIER = identifier_tags
    DEMOGRAPHIC = demographic_tags
    INTEREST = interest_tags
    OUTCOME = outcome_tags
    WHAT_YOU_SEEK = what_you_seek_tags
    SELF_PERCEPTION = self_perception_tags
    RATINGS_GIVEN = ratings_given_tags


class col:
    # === IDENTIFIERS ===
    iid = Col("iid", "Unique participant ID", "int", group=Group.IDENTIFIER)
    id = Col("id", "ID within wave", "float", group=Group.IDENTIFIER)
    gender = Col("gender", "0 = female, 1 = male", "int", group=Group.IDENTIFIER)
    wave = Col("wave", "Wave number 1-21", "int", group=Group.IDENTIFIER)
    pid = Col("pid", "Partner's iid", "float", group=Group.IDENTIFIER)
    partner = Col("partner", "Partner number this round", "int", group=Group.IDENTIFIER)

    # === DEMOGRAPHICS ===
    age = Col("age", "Age", "float", group=Group.DEMOGRAPHIC)
    race = Col(
        "race",
        "Race (1=Black,2=White,3=Latino,4=Asian,5=Other)",
        "float",
        group=Group.DEMOGRAPHIC,
    )
    imprace = Col(
        "imprace", "Importance of same race (1-10)", "float", group=Group.DEMOGRAPHIC
    )
    imprelig = Col(
        "imprelig",
        "Importance of same religion (1-10)",
        "float",
        group=Group.DEMOGRAPHIC,
    )
    income = Col("income", "Household income", "float", group=Group.DEMOGRAPHIC)
    goal = Col("goal", "Main goal in participating", "float", group=Group.DEMOGRAPHIC)
    date = Col(
        "date", "Dating frequency (1=often → 7=never)", "float", group=Group.DEMOGRAPHIC
    )
    go_out = Col("go_out", "How often you go out", "float", group=Group.DEMOGRAPHIC)
    field_cd = Col(
        "field_cd", "Field of study (coded)", "float", group=Group.DEMOGRAPHIC
    )
    career_c = Col(
        "career_c", "Intended career (coded)", "float", group=Group.DEMOGRAPHIC
    )

    # === INTERESTS (1-10) ===
    sports = Col("sports", "Interest in sports", "float", group=Group.INTERESTS)
    tvsports = Col(
        "tvsports", "Interest in watching sports", "float", group=Group.INTERESTS
    )
    exercise = Col("exercise", "Interest in exercise", "float", group=Group.INTERESTS)
    dining = Col("dining", "Interest in dining out", "float", group=Group.INTERESTS)
    museums = Col("museums", "Interest in museums", "float", group=Group.INTERESTS)
    art = Col("art", "Interest in art", "float", group=Group.INTERESTS)
    hiking = Col("hiking", "Interest in hiking", "float", group=Group.INTERESTS)
    gaming = Col("gaming", "Interest in gaming", "float", group=Group.INTERESTS)
    clubbing = Col("clubbing", "Interest in clubbing", "float", group=Group.INTERESTS)
    reading = Col("reading", "Interest in reading", "float", group=Group.INTERESTS)
    tv = Col("tv", "Interest in TV", "float", group=Group.INTERESTS)
    theater = Col("theater", "Interest in theater", "float", group=Group.INTERESTS)
    movies = Col("movies", "Interest in movies", "float", group=Group.INTERESTS)
    concerts = Col("concerts", "Interest in concerts", "float", group=Group.INTERESTS)
    music = Col("music", "Interest in music", "float", group=Group.INTERESTS)
    shopping = Col("shopping", "Interest in shopping", "float", group=Group.INTERESTS)
    yoga = Col("yoga", "Interest in yoga", "float", group=Group.INTERESTS)

    # === WHAT YOU SEEK (the 6 core attributes) ===
    attr1_1 = Col(
        "attr1_1", "Attractiveness you seek (time 1)", "float", group=Group.PREFERENCE
    )
    sinc1_1 = Col("sinc1_1", "Sincerity you seek", "float", group=Group.PREFERENCE)
    intel1_1 = Col("intel1_1", "Intelligence you seek", "float", group=Group.PREFERENCE)
    fun1_1 = Col("fun1_1", "Fun you seek", "float", group=Group.PREFERENCE)
    amb1_1 = Col("amb1_1", "Ambition you seek", "float", group=Group.PREFERENCE)
    shar1_1 = Col("shar1_1", "Shared hobbies you seek", "float", group=Group.PREFERENCE)

    # === SELF-PERCEPTION ===
    attr3_1 = Col(
        "attr3_1",
        "How attractive you rate yourself",
        "float",
        group=Group.SELF_PERCEPTION,
    )
    sinc3_1 = Col(
        "sinc3_1", "How sincere you rate yourself", "float", group=Group.SELF_PERCEPTION
    )
    intel3_1 = Col(
        "intel3_1",
        "How intelligent you rate yourself",
        "float",
        group=Group.SELF_PERCEPTION,
    )
    fun3_1 = Col(
        "fun3_1", "How fun you rate yourself", "float", group=Group.SELF_PERCEPTION
    )
    amb3_1 = Col(
        "amb3_1",
        "How ambitious you rate yourself",
        "float",
        group=Group.SELF_PERCEPTION,
    )

    # === RATINGS YOU GAVE TO PARTNER ===
    attr = Col("attr", "Rated partner: attractive", "float")
    sinc = Col("sinc", "Rated partner: sincere", "float")
    intel = Col("intel", "Rated partner: intelligent", "float")
    fun = Col("fun", "Rated partner: fun", "float")
    amb = Col("amb", "Rated partner: ambitious", "float")
    shar = Col("shar", "Rated partner: shared hobbies", "float")
    like = Col("like", "Overall how much you liked partner", "float")
    prob = Col("prob", "How much you think partner likes you", "float")

    # === OUTCOME ===
    match = Col("match", "Both said yes", "int")
    dec = Col("dec", "You said yes", "int")
    dec_o = Col("dec_o", "Partner said yes to you", "int")


def to_list() -> List[Col]:
    return [getattr(col, attr) for attr in dir(col) if not attr.startswith("__")]


def get_col_by_name(name: str) -> Col | None:
    for c in to_list():
        if c.name == name:
            return c
    return None


def exists(key: str) -> bool:
    return get_col_by_name(key) is not None


def list_groups() -> List[Group]:
    groups = set()
    for c in to_list():
        if c.group is not None:
            groups.add(c.group)
    return list(groups)


def list_by_group(group: Group | str) -> List[Col]:
    result = []
    for c in to_list():
        if c.group == group:
            result.append(c)
    return result


def list_by_tags(*tags) -> List[Col]:
    result = []
    for c in to_list():
        if c.tags is not None and all(tag in c.tags for tag in tags):
            result.append(c)
    return result


# ================================================================
# HELPER FUNCTIONS - return list of column NAMES (dot-accessible)
# ================================================================
def interests() -> List[str]:
    return [
        col.sports.name,
        col.tvsports.name,
        col.exercise.name,
        col.dining.name,
        col.museums.name,
        col.art.name,
        col.hiking.name,
        col.gaming.name,
        col.clubbing.name,
        col.reading.name,
        col.tv.name,
        col.theater.name,
        col.movies.name,
        col.concerts.name,
        col.music.name,
        col.shopping.name,
        col.yoga.name,
    ]


def what_you_seek() -> List[str]:
    return [
        col.attr1_1.name,
        col.sinc1_1.name,
        col.intel1_1.name,
        col.fun1_1.name,
        col.amb1_1.name,
        col.shar1_1.name,
    ]


def self_perception() -> List[str]:
    return [
        col.attr3_1.name,
        col.sinc3_1.name,
        col.intel3_1.name,
        col.fun3_1.name,
        col.amb3_1.name,
    ]


def ratings_given() -> List[str]:
    return [
        col.attr.name,
        col.sinc.name,
        col.intel.name,
        col.fun.name,
        col.amb.name,
        col.shar.name,
        col.like.name,
    ]


def demographics() -> List[str]:
    return [
        col.gender.name,
        col.age.name,
        col.race.name,
        col.imprace.name,
        col.imprelig.name,
        col.income.name,
        col.goal.name,
        col.go_out.name,
    ]


def outcome() -> List[str]:
    return [col.match.name, col.dec.name, col.dec_o.name]
