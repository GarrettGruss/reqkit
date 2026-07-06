from reqkit.parser import parse_str
from reqkit.types import ReqkitRequirement, ReqkitTrace


def test_parses_valid_requirement_tag():
    text = '<rq-req id="3a5cf8" subtype="fr" category="my_cat">do the thing</rq-req>'

    objs = parse_str(text)

    assert len(objs) == 1
    assert isinstance(objs[0], ReqkitRequirement)
    assert objs[0].id == "3a5cf8"
    assert objs[0].subtype == "fr"
    assert objs[0].category == "my_cat"
    assert objs[0].body == "do the thing"

def test_parses_special_characters():
    text = '<rq-req id="3a5cf8" subtype="fr" category="my_cat">x = 4 // 2 if 4 > 2 else x = 2</rq-req>'

    objs = parse_str(text)

    assert len(objs) == 1
    assert isinstance(objs[0], ReqkitRequirement)
    assert objs[0].id == "3a5cf8"
    assert objs[0].subtype == "fr"
    assert objs[0].category == "my_cat"
    assert objs[0].body == "x = 4 // 2 if 4 > 2 else x = 2"


def test_parses_valid_trace_tag():
    text = '<rq-trace parent_id="3a5cf8" parent_rel="derive">trace body</rq-trace>'

    objs = parse_str(text)

    assert len(objs) == 1
    assert isinstance(objs[0], ReqkitTrace)
    assert objs[0].parent_id == "3a5cf8"
    assert objs[0].parent_rel == "derive"
    assert objs[0].body == "trace body"


def test_parses_self_closing_tag():
    text = '<rq-trace parent_id="3a5cf8" parent_rel="derive" />'

    objs = parse_str(text)

    assert len(objs) == 1
    assert objs[0].body is None


def test_skips_malformed_xml(capsys):
    text = '<rq-req id="3a5cf8 subtype="fr" category="my_cat"></rq-req>'

    objs = parse_str(text)

    assert objs == []
    assert "failed xml parsing" in capsys.readouterr().out


def test_skips_invalid_subtype(capsys):
    text = '<rq-req id="3a5cf8" subtype="bogus"></rq-req>'

    objs = parse_str(text)

    assert objs == []
    assert "failed validation" in capsys.readouterr().out


def test_skips_invalid_parent_rel(capsys):
    text = '<rq-trace parent_id="3a5cf8" parent_rel="bogus"></rq-trace>'

    objs = parse_str(text)

    assert objs == []
    assert "failed validation" in capsys.readouterr().out


def test_extracts_tags_from_surrounding_prose():
    text = """
    Some markdown prose here that is not xml at all.

    <rq-req id="3a5cf8" subtype="fr" category="my_cat">do the thing</rq-req>

    More prose, and a trace below.

    <rq-trace parent_id="3a5cf8" parent_rel="derive">trace body</rq-trace>
    """

    objs = parse_str(text)

    assert len(objs) == 2
    assert isinstance(objs[0], ReqkitRequirement)
    assert isinstance(objs[1], ReqkitTrace)


def test_skips_malformed_but_keeps_valid_tags():
    text = """
    <rq-req id="3a5cf8" subtype="fr">do the thing</rq-req>
    <rq-req id="3a5cf8 subtype="fr" category="my_cat"></rq-req>
    <rq-trace parent_id="3a5cf8" parent_rel="derive">trace body</rq-trace>
    """

    objs = parse_str(text)

    assert len(objs) == 2
