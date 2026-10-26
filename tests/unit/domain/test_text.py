from adr_toolkit.domain.text import has_figure, sentences, similarity, squash, words


def test_squash_collapses_whitespace():
    assert squash("a \n b\t c") == "a b c"


def test_sentences_split_on_full_stops_before_a_capital_or_digit():
    assert sentences("One. Two! Three? four") == ["One.", "Two!", "Three? four"]


def test_sentences_of_nothing_is_empty():
    assert sentences("   ") == []


def test_words_are_lower_case_and_keep_apostrophes():
    assert words("The relay's Backlog, 1,000") == ["the", "relay's", "backlog", "1", "000"]


def test_has_figure_finds_a_digit():
    assert has_figure("40,000 orders")
    assert not has_figure("many orders")


def test_similarity_runs_from_zero_to_one():
    assert similarity("a b c", "a b c") == 1.0
    assert similarity("a b", "c d") == 0.0
    assert similarity("", "a") == 0.0
